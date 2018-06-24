# encoding:utf-8
from app import rpc
from app.test.default import DefaultExchange
from app.test.topic import CheckResultRpc

rpc.register_class(CheckResultRpc)
rpc.register_class(DefaultExchange)

rpc.run()