# encoding:utf-8
from flask_rabbitmq.util._logger import logger
from . import ExchangeType
import uuid
import time
import threading
import json
import pika

class RabbitMQ(object):

    def __init__(self, app=None, queue=None):
        self.app = app
        self.queue = queue
        self.config = self.app.config

        self.rabbitmq_server_host = None
        self.rabbitmq_server_username = None
        self.rabbitmq_server_password = None

        self._connection = None
        self._channel = None
        self._rpc_class_list = []
        self.data = {}
        # initialize some operation
        self.init()

    def init(self):
        self.valid_config()
        self.connect_rabbitmq_server()

    # valid config value such as server host, username and password
    def valid_config(self):
        if not self.config.get('RABBITMQ_HOST'):
            raise Exception("The rabbitMQ application must configure host.")
        self.rabbitmq_server_host = self.config.get('RABBITMQ_HOST')
        self.rabbitmq_server_username = self.config.get('RABBITMQ_USERNAME')
        self.rabbitmq_server_password = self.config.get('RABBITMQ_PASSWORD')

    # connect RabbitMQ server
    def connect_rabbitmq_server(self):
        if not (self.rabbitmq_server_username and self.rabbitmq_server_password):
            # connect RabbitMQ server with no authentication
            self._connection = pika.BlockingConnection()
        elif (self.rabbitmq_server_username and self.rabbitmq_server_password):
            # connect RabbitMQ server with authentication
            credentials = pika.PlainCredentials(
                self.rabbitmq_server_username,
                self.rabbitmq_server_password
            )
            self._connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    self.rabbitmq_server_host,
                    credentials=credentials
                ))
        else:
            raise Exception()
        # create channel object
        self._channel = self._connection.channel()

    def temporary_queue_declare(self):
        """
        declare a temporary queue that named random string
        and will automatically deleted when we disconnect the consumer
        :return: the name of temporary queue like amq.gen-4NI42Nw3gJaXuWwMxW4_Vg
        """
        return self.queue_declare(exclusive=True,
                                  auto_delete=True)

    def queue_declare(self, queue_name='', passive=False, durable=False,
                      exclusive=False, auto_delete=False, arguments=None):
        result = self._channel.queue_declare(
            queue=queue_name,
            passive=passive,
            durable=durable,
            exclusive=exclusive,
            auto_delete=auto_delete,
            arguments=arguments
        )
        return result.method.queue

    def exchange_bind_to_queue(self, type, exchange_name, routing_key, queue):
        """
        Declare exchange and bind queue to exchange
        :param type: The type of exchange
        :param exchange_name: The name of exchange
        :param routing_key: The key of exchange bind to queue
        :param queue: queue name
        """
        self._channel.exchange_declare(exchange=exchange_name,
                                       exchange_type=type)
        self._channel.queue_bind(queue=queue,
                                 exchange=exchange_name,
                                 routing_key=routing_key)

    def basic_consuming(self, queue_name, callback):
        self._channel.basic_consume(
            consumer_callback=callback,
            queue=queue_name
        )

    def consuming(self):
        self._channel.start_consuming()

    def send(self, body, exchange, key, corr_id=None):
        if not corr_id:
            self._channel.basic_publish(
                exchange=exchange,
                routing_key=key,
                body=body
            )
        else:
            self._channel.basic_publish(
                exchange=exchange,
                routing_key=key,
                body=body,
                properties=pika.BasicProperties(
                    correlation_id=corr_id
                )
            )

    def send_json(self, body, exchange, key, corr_id=None):
        data = json.dumps(body)
        self.send(data, exchange=exchange, key=key, corr_id=corr_id)

    # Send message to server synchronously（just like Remote Procedure Call）
    def send_sync(self, body, key=None, timeout=5):
        if not key:
            raise Exception("The routing key is not present.")
        corr_id = str(uuid.uuid4())  # generate correlation id
        callback_queue = self.temporary_queue_declare() # 得到随机回调队列名
        self.data[corr_id] = {
            'isAccept': False,
            'result': None,
            'reply_queue_name': callback_queue
        }
        # Client consume reply_queue
        self._channel.basic_consume(self.on_response,
                                    no_ack=True,
                                    queue=callback_queue)
        # send message to queue that server is consuming
        self._channel.basic_publish(
            exchange='',
            routing_key=key,
            body=body,
            properties=pika.BasicProperties(
                reply_to=callback_queue,
                correlation_id=corr_id,
            )
        )

        end = time.time() + timeout
        while time.time() < end:
            if self.data[corr_id]['isAccept']:  # 判断是否接收到服务端返回的消息
                logger.info("Got the RPC server response => {}".format(self.data[corr_id]['result']))
                return self.data[corr_id]['result']
            else:
                self._connection.process_data_events()
                time.sleep(0.3)
                continue
        # 超时处理
        logger.error("Get the response timeout.")
        return None

    def send_json_sync(self, body, key=None):
        if not key:
            raise Exception("The routing key is not present.")
        data = json.dumps(body)
        return self.send_sync(data, key=key)

    def accept(self, key, result):
        """
        同步接受确认消息
        :param key: correlation_id
        :param result 服务端返回的消息
        """
        self.data[key]['isAccept'] = True # 设置为已经接受到服务端返回的消息
        self.data[key]['result'] = str(result)
        self._channel.queue_delete(self.data[key]['reply_queue_name'])  # 删除客户端声明的回调队列

    def on_response(self, ch, method, props, body):
        """
        所有的RPC请求回调都会调用该方法，在该方法内修改对应corr_id已经接受消息的isAccept值和返回结果
        """
        logger.info("on response => {}".format(body))

        corr_id = props.correlation_id  # 从props得到服务端返回的客户度传入的corr_id值
        self.accept(corr_id, body)

    def register_class(self, rpc_class):
        if not hasattr(rpc_class, 'declare'):
            raise AttributeError("The registered class must contains the declare method")
        self._rpc_class_list.append(rpc_class)

    def _run(self):
        # register queues and declare all of exchange and queue
        for item in self._rpc_class_list:
            item().declare()
        for (type, queue_name, exchange_name, routing_key, callback) in self.queue._rpc_class_list:
            if type == ExchangeType.DEFAULT:
                if not queue_name:
                    # If queue name is empty, then declare a temporary queue
                    queue_name = self.temporary_queue_declare()
                else:
                    self._channel.queue_declare(queue=queue_name, auto_delete=True)
                    self.basic_consuming(queue_name, callback)

            if type == ExchangeType.FANOUT or type == ExchangeType.DIRECT or type == ExchangeType.TOPIC:
                if not queue_name:
                    # If queue name is empty, then declare a temporary queue
                    queue_name = self.temporary_queue_declare()
                else:
                    self._channel.queue_declare(queue=queue_name)
                self.exchange_bind_to_queue(type, exchange_name, routing_key, queue_name)
                # Consume the queue
                self.basic_consuming(queue_name, callback)

        logger.info(" * The flask RabbitMQ application is consuming")
        t = threading.Thread(target = self.consuming)
        t.start()

    # run the consumer application
    def run(self):
        self._run()

    # run the consumer application with flask application
    def run_with_flask_app(self, host = "localhost", port=5000):
        self._run()
        self.app.run(host, port)