# encoding:utf-8
from app import app
from app import rpc

@app.route('/')
def test():
    data = {
        'userName':'Pushy'
    }
    rpc.send_json_string(
        data,
        exchange='s4t-checkResult-exchange',
        key='s4t-checkResult-key-good'
    )
    return 'ok'