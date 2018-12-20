## RPC

`flask-rabbit`也支持RPC的方式通信，需要进行如下的额外的操作。

### 1. Client

我们先定义一个路由，在该视图函数的逻辑中通过`send_json_sync`方法同步地调用服务端的方法：

```python
@app.route('/sum/sync')
def sync_sum():
    a = request.args.get('a', type=int)
    b = request.args.get('b', type=int)
    if not a or not b:
        return 'lack param'
    data = {'a':a, 'b':b}
    # 通过同步的方法来发送，result即同步请求生产者返回的响应
    result = rpc.send_json_sync(data, exchange='', key='rpc-queue')
    return result
```

### 2. Server

该服务端被调用的方法中，在处理完业务逻辑之后，需要`send_json`方法将处理的结果发送到客户端监听的队列中。并且需要多传一个`corr_id`参数的值：

```python
@queue(queue_name='rpc-queue')
def sum_callback(ch, method, props, body):
    data = json.loads(body)
    result = data['a'] + data['b']  # 计算结果值
    data = {
        'result': result
    }
    
    # 确认接收消息，为rabbimq自带的机制
    ch.basic_ack(delivery_tag=method.delivery_tag)  
    rpc.send_json(data, 
                  exchange='', 
                  key=props.reply_to,  # 客户端监听的回调队列
                  corr_id=props.correlation_id)  # 返回客户端请求的id
```