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

# from huey import RedisHuey

# pool = redis.BlockingConnectionPool(host="redis", max_connections=5, timeout=None)
# huey = RedisHuey(name='app', connection_pool=pool)

# @huey.task()
# def test():
#     from time import sleep
#     # sleep(1)
#     print("All done")
#     return 42

from celery import Celery
from celery.result import AsyncResult
from celery.result import ResultBase
cel=Celery("Tasks", broker='redis://redis:6379/0', backend='redis://redis:6379/0')
cel.conf.broker_pool_limit = 1
cel.conf.redis_max_connections = 1

@cel.task()
def test():
    from time import sleep
    sleep(2)
    print("All done")
    return 42
