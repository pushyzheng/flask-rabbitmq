# encoding:utf-8
from flask_rabbitmq.util._logger import logger

# 定义交换机类型的枚举值
class ExchangeType():

    DEFAULT = 'default'
    TOPIC = 'topic'

def register_class(rpc):
    def decotator(cls):
        RabbitMQ.rpc_instance = rpc
        rpc.register_class(cls)
        return cls
    return decotator

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


from .RabbitMQ import RabbitMQ