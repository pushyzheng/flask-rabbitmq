# encoding:utf-8
from example.app import rpc,queue
from example.app.test.topic import CheckResultRpc
from example.app.test.default import DefaultExchange
from flask_rabbitmq import ExchangeType

# 通过注册类的形式进行声明
rpc.register_class(CheckResultRpc)
rpc.register_class(DefaultExchange)

# 通过装饰器的方式进行声明一个默认交换机的队列
@queue(queue_name='helloc')
def helloc_callback(ch, method, props, body):
    print(body)

# 通过装饰器的方式声明一个主题交换机，框架会自动将queue和exchange通过key绑定
@queue(queue_name='hello-topic', type=ExchangeType.TOPIC, exchange_name='hello-exchange',
       routing_key='hello-key')
def hellp_topic_callback(ch, method, props, body):
    print(body)

rpc.run()