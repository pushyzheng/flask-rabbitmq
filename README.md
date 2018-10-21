# flask-rabbitmq

`flask-rabbitmq` is a frame that simplifies python to operate rabbitmq and can be combined with Flask very well. So you don't need to think about the underlying operations

[中文文档点这](https://github.com/PushyZqin/flask-rabbitmq/blob/dev/documentation/%E4%B8%AD%E6%96%87README.md)

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

# declare the queue of topic exchange, flask-rabbitmq will bind automatically by key
@queue(queue_name='hello-topic', type=ExchangeType.TOPIC, exchange_name='hello-exchange',
       routing_key='hello-key')
def hellp_topic_callback(ch, method, props, body):
    print(body)

rpc.run()
```

## Contact me

Email：1437876073@qq.com

## License

```
MIT License

Copyright (c) 2018 Pushy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

