from app import app
from app import rpc
from flask import request

@app.route('/sum')
def index():
    a = request.args.get('a', type=int)
    b = request.args.get('b', type=int)
    data = {
        'a':a,
        'b':b
    }
    rpc.send_json(data,key='sum')
    return "ok"