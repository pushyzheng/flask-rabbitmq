# encoding:utf-8

# 定义交换机类型的枚举值
class ExchangeType():

    DEFAULT = 'default'
    DIRECT = "direct"
    FANOUT = "fanout"
    TOPIC = 'topic'


from .RabbitMQ import RabbitMQ
from .queue import Queue