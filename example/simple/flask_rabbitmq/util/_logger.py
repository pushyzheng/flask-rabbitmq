# encoding:utf-8
import logging

logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

pikaLogger = logging.getLogger('pika').setLevel(logging.WARNING)