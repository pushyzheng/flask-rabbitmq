#encoding:utf-8
from flask import Flask,appcontext_tearing_down
import config
from src import RabbitMQ

app = Flask(__name__)
app.config.from_object(config)

rpc = RabbitMQ(app)

from app import test
from app import views