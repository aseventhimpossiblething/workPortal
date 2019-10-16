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

the_redis=os.environ.get("REDIS_URL")
#print(the_redis)

#print("THIS SHOWS AS app <<<<<  in main doc",app)
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
#print("print celery",celery)

#print("THIS SHOWS AS app >>>>> after context is set",app)

  
@celery.task()
def initiLjoV():
  print("tasque File Running initiJoV")
  Rval="return value"
  return Rval
run_initiLjoV=initiLjoV.delay() 
print(run_initiLjoV)





