# encoding:utf-8
from src.demo import Demo
import threading

class Main():

    @classmethod
    def run(cls):
        d = Demo()
        # 开启一个子线程
        t = threading.Thread(target=d.run)
        t.start()