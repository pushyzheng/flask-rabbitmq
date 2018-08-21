## RPC

`flask-rabbit`也支持RPC的方式通信，需要进行额外的配置：

### 1. Client

我们先定义一个路由，在该视图函数的逻辑中通过`send_json_sync`方法同步地调用服务端的方法：

```python
# RPC（同步）
@app.route('/sum/sync')
def sync_sum():
    a = request.args.get('a', type=int)
    b = request.args.get('b', type=int)
    if not a or not b:
        return 'lack param'
    data = {'a':a, 'b':b}
    # 通过同步的方法来发送
    result = rpc.send_json_sync(data, exchange='sum-exchange', key='sum-key')
    return result
```

因为是同步的调用，我们需要在客户端声明一个队列回调函数；该回调函数是服务端被调用的方法返回的队列调用的，在方法内需要通过`accept`方法来确认接收消息：

```python
@queue(queue_name='sum-result', type=ExchangeType.TOPIC,
       exchange_name='sum-result-exchange',routing_key='sum-result-key')
def sum_callback(ch, method, props, body):
    logging.info("correlation_id - " + props.correlation_id)
    logging.info("body - " + body)
    rpc.accept(props.correlation_id, body)
```

### 2. Server

该服务端被调用的方法中，在处理完业务逻辑之后，需要`send_json`方法将处理的结果发送到客户端监听的队列中。并且需要多传一个`corr_id`参数的值：

```python
@queue(queue_name='sum', type=ExchangeType.TOPIC,
       exchange_name='sum-exchange', routing_key='sum-key')
def sum_callback(ch, method, props, body):
    print(props.correlation_id)
    data = json.loads(body)
    result = data['a'] + data['b']
    print("Result -- " + str(result))
    data = {
        'result': result
    }
    rpc.send_json(data, exchange='sum-result-exchange', key='sum-result-key', corr_id=props.correlation_id)
```