# encoding:utf-8
from app import rpc
from app import app

class CheckResultRpc(object):

    def __init__(self):
        self.data = app.config.get('RPC_DATA')

    def callback_a(self, ch, method, props, body):
        print(str(body))

    def declare2(self):
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