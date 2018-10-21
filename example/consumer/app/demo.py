# encoding:utf-8
from app import rpc,queue
from flask_rabbitmq import ExchangeType
import logging

@queue(queue_name='sum-result', type=ExchangeType.TOPIC,
       exchange_name='sum-result-exchange',routing_key='sum-result-key')
def sum_callback(ch, method, props, body):
    logging.info("correlation_id - " + props.correlation_id)
    logging.info("body - " + body)
    rpc.accept(props.correlation_id, body)

rpc.run()