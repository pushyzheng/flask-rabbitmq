# encoding:utf-8
from app import app
from app import rpc
from flask import request

@app.route('/')
def index():
    return 'Hello World'

# 消息队列（异步）
@app.route('/sum')
def sum():
    a = request.args.get('a', type=int)
    b = request.args.get('b', type=int)
    if not a or not b:
        return 'lack param'
    data = {'a':a, 'b':b}
    rpc.send_json(data, exchange='sum-exchange', key='sum-key')
    return "ok"

# RPC（同步）
@app.route('/sum/sync')
def sync_sum():
    a = request.args.get('a', type=int)
    b = request.args.get('b', type=int)
    if not a or not b:
        return 'lack param'
    data = {'a':a, 'b':b}
    # 通过同步的方法来发送
    result = rpc.send_json_sync(data, exchange='', key='rpc-queue')
    return result