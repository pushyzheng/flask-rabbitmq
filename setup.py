from setuptools import setup

setup(
    name='flask-rabbitmq',
    version='0.0.7',
    author='Pushy',
    author_email='1437876073@qq.com',
    url='https://github.com/PushyZqin/flask-rabbitmq',
    description=u'Let rabbitmq use flask development more easy! ! !',
    packages=['flask_rabbitmq'],
    install_requires=['pika']
)