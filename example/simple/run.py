#encoding:utf-8
from app import app
from app import rpc

if __name__ == '__main__':
    rpc.run()
    app.run(debug=True)