# encoding:utf-8
from app import rpc
from app.test.demo import CheckResultRpc

rpc.register_class(CheckResultRpc)

rpc.run()

from app.test import demo