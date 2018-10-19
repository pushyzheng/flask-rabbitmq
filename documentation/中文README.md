# flask-rabbitmq

`flask-rabbitmq`是一个简化Python的`rabbitmq`操作的框架，并且很好地和Flask结合，让你不需要去考虑底层的操作。


## Install

在项目已经提交到[Pypi](https://pypi.org/project/flask-rabbitmq/)上，可直接通过`pip`进行安装：

```
$ pip install flask-rabbitmq
```

## Features

- 跟随Flask应用启动，让开发者不需要考虑进程的阻塞

- 通过`config.py`配置连接，很好的与代码解耦

- 支持通过装饰器或注册类的方式声明队列，简化声明队列和消费的操作

## Simple example

首先在`app/__init__.py`在实例化`RabbitMQ`和`Queue`对象，然后导入`demo`的包文件：

```python
from example.app import app
from flask_rabbitmq import Queue
from flask_rabbitmq import RabbitMQ

queue = Queue()
rpc = RabbitMQ(app, queue)

from example.app import demo
```

在`app`目录下创建`demo`包，在`__init__`文件中声明队列和消费：

```python
from example.app import rpc,queue
from flask_rabbitmq import ExchangeType

# 通过装饰器的方式进行声明一个默认交换机的队列
@queue(queue_name='helloc')
def helloc_callback(ch, method, props, body):
    print(body)

# 通过装饰器的方式声明一个主题交换机，框架会自动将queue和exchange通过key绑定
@queue(queue_name='hello-topic', type=ExchangeType.TOPIC, exchange_name='hello-exchange',
       routing_key='hello-key')
def hellp_topic_callback(ch, method, props, body):
    print(body)

rpc.run()
```

## License

MIT