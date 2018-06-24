# encoding:utf-8
from app import rpc

class CheckResultRpc():

    def __init__(self):
        pass

    def callback_a(self, ch, method, props, body):
        print(str(body))

    def declare(self):
        for name in ['good','task']:
            exchange_name = 's4t-checkResult-exchange'
            queue_name = 's4t-checkResult-queue-{}'.format(name)
            routing_key = 's4t-checkResult-key-{}'.format(name)
            rpc.declare_consuming(
                exchange_name=exchange_name,
                queue_name=queue_name,
                routing_key=routing_key,
                callback=self.callback_a
            )