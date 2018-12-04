# Quick Start

## 1. 声明队列

在`flask-rabbitmq`中，声明队列有两种方式：

- 通过装饰器`@queue`声明队列。
- 通过注册类声明队列，扩展性强， 并能更好地结构化逻辑方法代码。

### 1.1 装饰器

通过装饰器声明队列非常简单，我们只需要用`@queue`来修饰一个回调方法：

```python
# 声明一个简单队列
@queue('simple')
def callback(ch, method, props, body):
    print(body)

# 声明一个主题交换机，并自动将队列和交换机通过key值绑定
@queue(queue_name='hello', 
       type=ExchangeType.TOPIC, 
       exchange_name='hello-exchange',
       routing_key='hello-key')
def callback2(ch, method, props, body):
    print(body)
```

### 1.2 注册类

#### 简单队列

如果通过注册类声明队列和交换机的方式，必须在注册类中声明`declare`方法，用来写声明绑定的逻辑。如果没有定义该方法，将会抛出一个`AttributeError`异常：

```python
class Simple(object):
    
    def callback(self, ch, method, props, body):
        print(body)

    def declare(self):
        rpc.declare_queue('simple2', auto_delete=True)  # 声明
        rpc.basic_consuming('simple2', self.callback)   # 消费
```

我们来可以通过`declare_default_consuming`更加便捷地实现声明队列同时消费该队列：

```python
rpc.declare_default_consuming('simple2', self.callback)
```

注意，我们还需要注册该类才能正确地声明指定的队列，`flask-rabbitmq`提供了两种注册的方式：

```python
from flask_rabbitmq import register_class

# 直接调用rpc的register_class方法进行注册
rpc.register_class(Simple)

# 通过@register_class装饰器来注册
@register_class(rpc)
class Simple(object):
    # other code
```

#### 主题交换机

如果我们想将队列和主题交换机通过`key`进行绑定，可以很方便地在`declare`中调用`bind_topic_exchange`方法来声明：

```python
class SimpleTopic():

    def callback(self, ch, method, props, body):
        print(body)

    def declare(self):
        # 绑定交换机，flask-rabbitmq会自动声明该队列
        rpc.bind_topic_exchange(queue_name='simple2-topic',
                                exchange_name='simple2-exchange',
                                routing_key='simple2-key')

        rpc.basic_consuming('simple2-topic', self.callback)  # 消费
```

同样，我们也得注册该类：

```python
rpc.register_class(SimpleTopic)
```