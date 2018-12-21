# encoding:utf-8
from app import app
from app import mq
from flask import request

@app.route('/')
def index():
    return 'Hello World'

# Message Queue (Async)
@app.route('/sum')
def sum():
    a = request.args.get('a', type=int)
    b = request.args.get('b', type=int)
    if not a or not b:
        return 'lack param'
    data = {'a':a, 'b':b}
    mq.send_json(data, exchange='sum-exchange', key='sum-key')
    return "ok"

# Remote Procedure Call (Sync)
@app.route('/sum/sync')
def sync_sum():
    a = request.args.get('a', type=int)
    b = request.args.get('b', type=int)
    if not a or not b:
        return 'lack param'
    data = {
        'a': a,
        'b': b
    }
    # send message synchronously
    result = mq.send_json_sync(data, key='rpc-queue')
    if not result:
        return "The server don't return anything."
    return result