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
from celery import Celery
from flask import Flask

#the_redis=os.environ.get("REDIS_URL")
the_redis=redis.from_url(os.environ.get("REDIS_URL"))


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=the_redis,
        broker=the_redis
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery




flask_app = Flask(__name__)
flask_app.config.update(
    CELERY_BROKER_URL=the_redis,
    CELERY_RESULT_BACKEND=the_redis
)
celery = make_celery(flask_app)

  
@celery.task()
def initiLjoV():
  print("tasque File Running initiJoV")
  Rval="return value"
  return Rval
redis.Redis().client_getname()
#run_initiLjoV=initiLjoV.delay()

#print("initiLjoV State 1",run_initiLjoV.state)
#redis.Redis().flushdb()
#print("ended redis")
#print(redis.scan())
"""
print("initiLjoV State 2",run_initiLjoV.state)
print("initiLjoV State 3",run_initiLjoV.state)
print("initiLjoV State 4",run_initiLjoV.state)
print("initiLjoV State 5",run_initiLjoV.state)
print("initiLjoV State 6",run_initiLjoV.state)
print("initiLjoV State 7",run_initiLjoV.state)
print("initiLjoV State 8",run_initiLjoV.state)
"""
#print("result",run_initiLjoV.result)






