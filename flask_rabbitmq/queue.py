# encoding:utf-8
from . import ExchangeType

class Queue():

    def __init__(self):
        self._rpc_class_list = []

    def __call__(self, queue_name, type = ExchangeType.DEFAULT,exchange_name = None, routing_key = None):
        """
        当Queue对象被调用时，如@queue()执行的操作
        :param queue_name: 队列名
        :param type: 交换机的类型
        :param exchange_name:
        :param routing_key:
        :return:
        """
        def _(func):
            self._rpc_class_list.append((type, queue_name, exchange_name, routing_key, func))
        return _