# encoding:utf-8
from example.app import rpc

class DefaultExchange(object):

    def __init__(self):
        pass

    def callback(self, ch, method, props, body):
        print(body)

    def declare(self):
        rpc.declare_default_consuming('hello', self.callback)
        # rpc.send(
        #     body='hello world', exchange='', key='hello'
        # )