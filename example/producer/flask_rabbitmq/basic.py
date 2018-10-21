# encoding:utf-8
from abc import ABCMeta, abstractmethod

class BasicQueue():

    __metaclass__ = ABCMeta

    @abstractmethod
    def declare(self):
        pass

class Test(BasicQueue):

    def declare(self):
        pass


if __name__ == '__main__':

    test = Test()
    test.declare()
