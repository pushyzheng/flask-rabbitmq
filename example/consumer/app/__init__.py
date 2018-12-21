#encoding:utf-8
import config
from flask import Flask
from flask_rabbitmq import RabbitMQ,Queue

app = Flask(__name__)
app.config.from_object(config)

queue = Queue()
mq = RabbitMQ(app, queue)

from app import views, demo