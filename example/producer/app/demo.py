# encoding:utf-8
from app import rpc, queue
from flask_rabbitmq import ExchangeType
import json

@queue(queue_name='sum', type=ExchangeType.TOPIC,
       exchange_name='sum-exchange', routing_key='sum-key')
def sum_callback(ch, method, props, body):
    print(props.correlation_id)

    data = json.loads(body)
    result = data['a'] + data['b']
    print("Result -- " + str(result))
    data = {
        'result': result
    }
    rpc.send_json(data, exchange='sum-result-exchange', key='sum-result-key', corr_id=props.correlation_id)

rpc.run()
