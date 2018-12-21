# encoding:utf-8
from app import mq, queue
from flask_rabbitmq import ExchangeType

@queue()
def simple_queue(ch, method, props, body):
    print("simple queue => {}".format(body))

@queue(type=ExchangeType.DEFAULT, queue="default_exchange")
def default(ch, method, props, body):
    print("default queue => {}".format(body))

@queue(type=ExchangeType.FANOUT, exchange='fanout_exchange')
def fanout(ch, method, props, body):
    print("fanout queue => {}".format(body))

@queue(type=ExchangeType.DIRECT, exchange="direct_exchange", routing_key="key1")
def direct_key1(ch, method, props, body):
    print("direct key1 queue => {}".format(body))

@queue(type=ExchangeType.DIRECT, exchange="direct_exchange", routing_key="key2")
def direct_key1(ch, method, props, body):
    print("direct key2 queue => {}".format(body))

@queue(type=ExchangeType.TOPIC, exchange='topic-exchange', routing_key='user.#')
def topic(ch, method, props, body):
    print("topic queue => {}".format(body))