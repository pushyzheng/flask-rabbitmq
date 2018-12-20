#encoding:utf-8
from flask import Flask
import config
from flask_rabbitmq import Queue, RabbitMQ

app = Flask(__name__)
app.config.from_object(config)

queue = Queue()
mq = RabbitMQ(app, queue)

from app import demo
