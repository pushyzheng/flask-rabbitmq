#encoding:utf-8
from flask import Flask
from example import config
from flask_rabbitmq import RabbitMQ
from flask_rabbitmq import Queue

app = Flask(__name__)
app.config.from_object(config)

queue = Queue()
rpc = RabbitMQ(app, queue)

from example.app import test
