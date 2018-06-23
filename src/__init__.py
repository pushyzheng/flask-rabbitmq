# encoding:utf-8
from src.util._logger import logger
import threading
import pika

class RabbitMQ(object):

    def __init__(self, app=None):
        self.app = app
        self.config = self.app.config
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

    def declare_basic_consuming(self, callback, queue_name):
        """
        声明消费
        :param func: 回调函数
        :return:
        """
        self._channel.basic_consume(callback, queue=queue_name)

    def declare_consuming(self, exchange_name, routing_key, queue_name, callback):
        self.bind_topic_exchange(exchange_name,routing_key,queue_name)
        self.declare_basic_consuming(
            queue_name=queue_name,
            callback=callback
        )

    def consuming(self):
        self._channel.start_consuming()

    def register_class(self, rpc_class):
        if not hasattr(RabbitMQ,'declare'):
            raise AttributeError("注册的类必须包含 declare 方法")
        self._rpc_class_list.append(rpc_class)

    def run(self):
        for item in self._rpc_class_list:
            item().called()
        logger.info("consuming...")
        t = threading.Thread(target = self.consuming)
        t.start()