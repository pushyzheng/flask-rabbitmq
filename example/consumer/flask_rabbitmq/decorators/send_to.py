# encoding:utf-8
from functools import wraps

def decorators(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper