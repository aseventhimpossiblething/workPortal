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
form celery import Celery


app = Celery('taskque', broker=os.environ['REDIS_URL'])
def initiLjov():
  print("tasque File Running initiJoV")
initijoV()  
  

#app.config['CELERY_BROKER_URL'] = os.environ['REDIS_URL']
#app.config['CELERY_RESULT_BACKEND'] = os.environ['REDIS_URL']
#celery = Celery(app.name, broker=os.environ['REDIS_URL'])
#celery.conf.update(app.config)

#print("Task loaded")
"""
print(os.environ['REDIS_URL'])

app.config['CELERY_BROKER_URL'] = os.environ['REDIS_URL']
app.config['CELERY_RESULT_BACKEND'] = os.environ['REDIS_URL']


celery = Celery(app.name, broker=os.environ['REDIS_URL'])
celery.conf.update(app.config)
"""


