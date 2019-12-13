"""
Need to determine state/status
Need to limit redis/celery connections
reliable redis/celery cmds
voir les log persistant
Separer les contenue static es dynamique
"""

import CommunityUpdatesProcess
import glob
import numpy
import scipy
import pandas
import BidOpAssist
import fileHandler
import redis
import os
from redis import Redis
from flask import Flask
import threading



from huey import RedisHuey, crontab

#pool = redis.BlockingConnectionPool(host="redis", max_connections=5, timeout=None)
#huey = RedisHuey(name='app', connection_pool=pool)


#my addition
the_redis=os.environ.get("REDIS_URL")
the_redis=the_redis.encode(encoding='ascii',errors='strict')
print("the_redis")
print(the_redis)
print(type(the_redis))



#huey = RedisHuey(name='bdx-api-link', host=the_redis)
huey = RedisHuey(name='bdx-api-link')

#@huey.task()
def test():
    from time import sleep
    # sleep(1)
    print("All done")
    return 42
#test()
print("the test thread should fire here")
test=threading.Thread(target=test)
test.start()
print("the test thread should fire here")


# from celery import Celery
# from celery.result import AsyncResult
# from celery.result import ResultBase

# the_redis=os.environ.get("REDIS_URL")

# cel=Celery("Tasks", broker=the_redis, backend=the_redis)
# cel.conf.broker_pool_limit = 0
# cel.conf.redis_max_connections = 1

# @cel.task()
# def test():
#     from time import sleep
#     sleep(2)
#     print("All done")
#     return 42
