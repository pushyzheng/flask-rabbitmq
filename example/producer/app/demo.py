# encoding:utf-8
from app import rpc, queue
import json

@queue(queue_name='rpc-queue')
def sum_callback(ch, method, props, body):
    print(props.correlation_id)

    data = json.loads(body)
    result = data['a'] + data['b']
    print("Result -- " + str(result))
    data = {
        'result': result
    }
    ch.basic_ack(delivery_tag=method.delivery_tag)
    rpc.send_json(data, exchange='', key=props.reply_to, corr_id=props.correlation_id)


class SampleQueue():

    pass

rpc.run()