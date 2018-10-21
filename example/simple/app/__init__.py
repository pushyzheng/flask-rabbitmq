#encoding:utf-8
import config
from flask import Flask
from flask_rabbitmq import Queue
from flask_rabbitmq import RabbitMQ

app = Flask(__name__)
app.config.from_object(config)

queue = Queue()
rpc = RabbitMQ(app, queue)

from app import views
from app import demo