# encoding:utf-8
from functools import wraps

def send_to(queue=''):
    def decorators(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            return result
        return wrapper
    return decorators