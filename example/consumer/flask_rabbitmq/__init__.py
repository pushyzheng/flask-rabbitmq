# encoding:utf-8
from flask_rabbitmq.util._logger import logger
from functools import wraps
import threading
import json
import pika

# 定义交换机类型的枚举值
class ExchangeType():

    DEFAULT = 'default'
    TOPIC = 'topic'

class Queue():

    def __init__(self):
        self._rpc_class_list = []

    def __call__(self, queue_name, type = 'default',exchange_name = None, routing_key = None):
        """
        当Queue对象被调用时，如@queue()执行的操作
        :param queue_name:
        :param type: 交换机的类型
        :param exchange_name:
        :param routing_key:
        :return:
        """
        logger.info("Queue callback called")
        def _(func):
            self._rpc_class_list.append((type, queue_name, exchange_name, routing_key, func))
        return _

class RabbitMQ(object):

    def __init__(self, app=None, queue=None):
        self.app = app
        self.queue = queue
        self.config = self.app.config
        if not (self.config.get('RPC_USER_NAME') and self.config.get('RPC_PASSWORD') and self.config.get('RPC_HOST')):
            logger.error('没有配置rpc服务器的用户名和密码')
            raise Exception
        self.credentials = pika.PlainCredentials(
            self.config['RPC_USER_NAME'],
            self.config['RPC_PASSWORD']
        )
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                self.config['RPC_HOST'],
                credentials=self.credentials
            ))
        self._channel = self._connection.channel()
        self._rpc_class_list = []

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

    def declare_queue(self, queue_name, passive=False, durable=False,
                      exclusive=False, auto_delete=False, arguments=None):
        self._channel.queue_declare(
            queue=queue_name,
            passive=passive,
            durable=durable,
            exclusive=exclusive,
            auto_delete=auto_delete,
            arguments=arguments
        )

    def declare_basic_consuming(self, queue_name, callback):
        self._channel.basic_consume(
            queue=queue_name,
            consumer_callback=callback
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
        self.declare_queue(
            queue_name=queue_name,passive=passive,
            durable=durable,exclusive=exclusive,
            auto_delete=auto_delete,arguments=arguments
        )
        self.declare_basic_consuming(
            queue_name=queue_name,
            callback=callback
        )

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
        self.declare_basic_consuming(
            queue_name=queue_name,
            callback=callback
        )

    def consuming(self):
        self._channel.start_consuming()

    def register_class(self, rpc_class):
        if not hasattr(rpc_class,'declare'):
            raise AttributeError("注册的类必须包含 declare 方法")
        self._rpc_class_list.append(rpc_class)

    def send(self, body, exchange, key):
        self._channel.basic_publish(
            exchange=exchange,
            routing_key=key,
            body=body
        )

    def send_json_string(self, body, exchange = '', key = None):
        data = json.dumps(body)
        self.send(data, exchange=exchange, key=key)

    def run(self):
        # 进行注册和声明
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
        logger.info("consuming...")
        t = threading.Thread(target = self.consuming)
        t.start()
