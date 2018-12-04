# encoding:utf-8
from app import queue
from app import rpc
from flask_rabbitmq import register_class
from flask_rabbitmq.decorators import send_to

@send_to('hello')
def send_to_hello():
    pass

@queue('simple')
def simple(ch, method, props, body):
    print(body)

class Simple():

    def callback(self, ch, method, props, body):
        print(body)

    def declare(self):
        rpc.declare_queue('simple2', auto_delete=True)
        rpc.basic_consuming('simple2', self.callback)

        # 或者直接通过declare_default_consuming 声明同时消费
        #rpc.declare_default_consuming('simple2', self.callback)

@register_class(rpc)
class SimpleTopic():

    def callback(self, ch, method, props, body):
        print(body)

    def declare(self):
        rpc.bind_topic_exchange(queue_name='simple2-topic',
                                exchange_name='simple2-exchange',
                                routing_key='simple2-key')

        rpc.basic_consuming('simple2-topic', self.callback)

rpc.register_class(Simple)