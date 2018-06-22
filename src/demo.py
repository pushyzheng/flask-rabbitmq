# encoding:utf-8
from src.util.logger import logger
from app import app
import pika

class Demo(object):

    def __init__(self):
        self.config = app.config
        self.credentials = pika.PlainCredentials(
            self.config['RPC_USER_NAME'],
            self.config['RPC_PASSWORD']
        )
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                self.config['RPC_HOST'],
                credentials=self.credentials
            ))
        self.channel = self.connection.channel()

    def bind_topic_exchange(self, exchange_name, routing_key, queue_name):
        self.channel.queue_declare(
            queue=queue_name,
            auto_delete=True,
            durable=True,
        )
        self.channel.exchange_declare(
            exchange=exchange_name,
            exchange_type='topic',
            auto_delete=True,
        )
        self.channel.queue_bind(
            exchange=exchange_name,
            queue=queue_name,
            routing_key=routing_key
        )

    def declare_consuming(self, func, queue_name):
        """
        声明消费
        :param func: 回调函数
        :return:
        """
        self.channel.basic_consume(func, queue=queue_name)

    def consuming(self):
        self.channel.start_consuming()

    def callback_a(self, ch, method, props, body):
        msg = str(body)
        logger.info("队列 a 收到消息 " + msg)

    def callback_b(self, ch, method, props, body):
        msg = str(body)
        logger.info("队列 b 收到消息 " + msg)

    def run(self):
        logger.info("绑定...")
        self.bind_topic_exchange('exchange_a', 'key_a', 'queue_a')
        self.bind_topic_exchange('exchange_b', 'key_b', 'queue_b')
        logger.info("监听...")
        self.declare_consuming(self.callback_a, 'queue_a')
        self.declare_consuming(self.callback_b, 'queue_b')

        self.consuming()

if __name__ == '__main__':
    f = Demo()
    f.run()

