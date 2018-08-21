# encoding:utf-8
from app import rpc

class DefaultExchange(object):

    def __init__(self):
        pass

    def callback(self, ch, method, props, body):
        print(body)

    def declare(self):
        # result = rpc.declare_queue('queue-', exclusive=True)
        # rpc.declare_basic_consuming(queue_name='queue-',callback=self.callback)
        pass