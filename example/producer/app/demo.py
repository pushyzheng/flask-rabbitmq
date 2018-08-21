# encoding:utf-8
from app import rpc,queue
from functools import wraps
import json

@queue('sum')
def sum_callback(ch, method, props, body):
    data = json.loads(body)
    result = data['a'] + data['b']
    print("Result -- " + str(result))

rpc.run()