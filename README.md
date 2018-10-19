# flask-rabbitmq

`flask-rabbitmq` is a frame that simplifies python to operate rabbitmq and can be combined with Flask very well. So you don't need to think about the underlying operations

## Install

This project has been commited to Pypi, can be installed by `pip`:

```shell
$ pip install flask-rabbitmq
```

## Features

- Start following Flask app, no consideration about the process blocking
- Configure by `config.py`
- Support declaring queue by decorator or register class

## Simple example

Firstly instantiate `RabbitMQ` and `Queue` object in `app/__init__.py` then import `demo` module:

```python
from example.app import app
from flask_rabbitmq import Queue
from flask_rabbitmq import RabbitMQ

queue = Queue()
rpc = RabbitMQ(app, queue)

from example.app import demo
```

Create `demo` package and `__init__.py`file in `app`directory. Now you can declare queue and consumer in `__init__.py`file:

```python
from example.app import rpc,queue
from flask_rabbitmq import ExchangeType

# declare the queue of defaulted exchange by decorator
@queue(queue_name='helloc')
def helloc_callback(ch, method, props, body):
    print(body)

# declare the queue of topic exchange, flask-rabbitmq will bind automatically
@queue(queue_name='hello-topic', type=ExchangeType.TOPIC, exchange_name='hello-exchange',
       routing_key='hello-key')
def hellp_topic_callback(ch, method, props, body):
    print(body)

rpc.run()
```

## License

MIT