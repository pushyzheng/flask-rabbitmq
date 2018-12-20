# encoding:utf-8

import time

end = time.time() + 5

while time.time() < end:
    print('waiting...')