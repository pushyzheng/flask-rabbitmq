# encoding:utf-8
from app import rpc,queue
from app.test.topic import CheckResultRpc
from app.test.default import DefaultExchange
from flask_rabbitmq import ExchangeType

# 通过注册类的形式进行声明
rpc.register_class(CheckResultRpc)
rpc.register_class(DefaultExchange)

# 通过装饰器的方式进行声明
@queue(queue_name='helloc')
def helloc_callback(ch, method, props, body):
    print(body)

@queue(queue_name='hello-topic', type=ExchangeType.TOPIC, exchange_name='hello-exchange',
       routing_key='hello-key')
def hellp_topic_callback(ch, method, props, body):
    print(body)

rpc.run()