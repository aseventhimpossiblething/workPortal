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

print("THIS SHOWS AS app <<<<< before context is set",app)
def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
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
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)
celery = make_celery(flask_app)

print("THIS SHOWS AS app >>>>> after context is set",app)

  
@celery.task()
def initiLjoV():
  print("tasque File Running initiJoV")
initiLjoV()  




"""
app = Celery('taskque', broker=os.environ['REDIS_URL'])
@app.task
def initiLjoV():
  print("tasque File Running initiJoV")
initiLjoV()  
  

#app.config['CELERY_BROKER_URL'] = os.environ['REDIS_URL']
#app.config['CELERY_RESULT_BACKEND'] = os.environ['REDIS_URL']
#celery = Celery(app.name, broker=os.environ['REDIS_URL'])
#celery.conf.update(app.config)

#print("Task loaded")

print(os.environ['REDIS_URL'])

app.config['CELERY_BROKER_URL'] = os.environ['REDIS_URL']
app.config['CELERY_RESULT_BACKEND'] = os.environ['REDIS_URL']


celery = Celery(app.name, broker=os.environ['REDIS_URL'])
celery.conf.update(app.config)
"""


