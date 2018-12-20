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

    def bind_topic_exchange(self, exchange_name, routing_key, queue_name):
        """
        绑定主题交换机和队列
        :param exchange_name: 需要绑定的交换机名
        :param routing_key:
        :param queue_name: 需要绑定的交换机队列名
        :return:
        """
        self._channel.queue_declare(
            queue=queue_name,
            auto_delete=True,
            durable=True,
        )
        self._channel.exchange_declare(
            exchange=exchange_name,
            exchange_type='topic',
            auto_delete=True,
        )
        self._channel.queue_bind(
            exchange=exchange_name,
            queue=queue_name,
            routing_key=routing_key
        )

    def declare_queue(self, queue_name='', passive=False, durable=False,
                      exclusive=False, auto_delete=False, arguments=None):
        """
        声明一个队列
        :param queue_name: 队列名
        :param passive:
        :param durable:
        :param exclusive:
        :param auto_delete:
        :param arguments:
        :return: pika 框架生成的随机回调队列名
        """
        result = self._channel.queue_declare(
            queue=queue_name,
            passive=passive,
            durable=durable,
            exclusive=exclusive,
            auto_delete=auto_delete,
            arguments=arguments
        )
        return result.method.queue

    def basic_consuming(self, queue_name, callback):
        self._channel.basic_consume(
            consumer_callback=callback,
            queue=queue_name
        )

    def declare_default_consuming(self, queue_name, callback, passive=False,
                                  durable=False,exclusive=False, auto_delete=False,
                                  arguments=None):
        """
        声明一个默认的交换机的队列，并且监听这个队列
        :param queue_name:
        :param callback:
        :return:
        """
        result = self.declare_queue(
            queue_name=queue_name,passive=passive,
            durable=durable,exclusive=exclusive,
            auto_delete=auto_delete,arguments=arguments
        )
        self.basic_consuming(
            queue_name=queue_name,
            callback=callback
        )
        return result

    def declare_consuming(self, exchange_name, routing_key, queue_name, callback):
        """
        声明一个主题交换机队列，并且将队列和交换机进行绑定，同时监听这个队列
        :param exchange_name:
        :param routing_key:
        :param queue_name:
        :param callback:
        :return:
        """
        self.bind_topic_exchange(exchange_name, routing_key, queue_name)
        self.basic_consuming(
            queue_name=queue_name,
            callback=callback
        )

    def consuming(self):
        self._channel.start_consuming()

    def register_class(self, rpc_class):
        if not hasattr(rpc_class, 'declare'):
            raise AttributeError("The registered class must contains the declare method")
        self._rpc_class_list.append(rpc_class)

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

    def send_sync(self, body, exchange, key, timeout=5):
        """
        发送并同步接受回复消息
        :return:
        """
        callback_queue = self.declare_queue(exclusive=True,
                                            auto_delete=True)  # 得到随机回调队列名
        self._channel.basic_consume(self.on_response,   # 客户端消费回调队列
                                    no_ack=True,
                                    queue=callback_queue)

        corr_id = str(uuid.uuid4())  # 生成客户端请求id
        self.data[corr_id] = {
            'isAccept': False,
            'result': None,
            'callbackQueue': callback_queue
        }
        self._channel.basic_publish( # 发送数据给服务端
            exchange=exchange,
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
                time.sleep(0.3)
                continue
        # 超时处理
        logger.error("Get the response timeout.")
        return None

    def accept(self, key, result):
        """
        同步接受确认消息
        :param key: correlation_id
        :param result 服务端返回的消息
        """
        self.data[key]['isAccept'] = True # 设置为已经接受到服务端返回的消息
        self.data[key]['result'] = str(result)
        self._channel.queue_delete(self.data[key]['callbackQueue'])  # 删除客户端声明的回调队列

    def on_response(self, ch, method, props, body):
        """
        所有的RPC请求回调都会调用该方法，在该方法内修改对应corr_id已经接受消息的isAccept值和返回结果
        """
        logger.info("on response => {}".format(body))

        corr_id = props.correlation_id  # 从props得到服务端返回的客户度传入的corr_id值
        self.accept(corr_id, body)

    def send_json_sync(self, body, exchange, key):
        data = json.dumps(body)
        return self.send_sync(data, exchange=exchange, key=key)

    def _run(self):
        # register queues and declare all of exchange and queue
        for item in self._rpc_class_list:
            item().declare()
        for (type, queue_name, exchange_name, routing_key, callback) in self.queue._rpc_class_list:
            if type == ExchangeType.DEFAULT:
                self.declare_default_consuming(
                    queue_name=queue_name,
                    callback=callback
                )
            if type == ExchangeType.TOPIC:
                self.declare_consuming(
                    queue_name=queue_name,
                    exchange_name=exchange_name,
                    routing_key=routing_key,
                    callback=callback
                )
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