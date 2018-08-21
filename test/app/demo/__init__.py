# encoding:utf-8
from app import rpc,queue
from app.demo.topic import TopicExchange
from app.demo.default import DefaultExchange
from flask_rabbitmq import ExchangeType

# 通过注册类的形式进行声明，这样可以实现多个队列使用同一个回调函数
rpc.register_class(TopicExchange)
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