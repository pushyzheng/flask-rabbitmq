# encoding:utf-8
from functools import wraps

def rpc_server(data_type='json', queue_name=''):
    def decorators(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)
        return wrapper
    return decorators