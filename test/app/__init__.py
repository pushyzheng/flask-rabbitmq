#encoding:utf-8
import config
from flask import Flask
from flask_rabbitmq import RabbitMQ
from flask_rabbitmq import Queue

app = Flask(__name__)
app.config.from_object(config)

queue = Queue()
rpc = RabbitMQ(app, queue)

from app import views,demo
