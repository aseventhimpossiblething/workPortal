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
from celery.result import AsyncResult
from celery.result import ResultBase

#print("++++++++++++++++++++++++++++++++++++",app.name())
#print("++++++++++++++++++++++++++++++++++++",app.name)



#print(Redis)    
#the_redis='redis://localhost:6379/0'
the_redis=os.environ.get("REDIS_URL")
print("This is the first attempt to connect Next is the REDIS_URL print?")
#the_redis=redis.from_url(os.environ.get("REDIS_URL"))
print("the_redis-----------------------",the_redis)

#print('setting 1 - os.environ.get("REDIS_URL")',os.environ.get("REDIS_URL"))
#print('current - setting 2 - redis.from_url(os.environ.get("REDIS_URL"))__:-->',redis.from_url(os.environ.get("REDIS_URL")))

#cel=Celery("TaskName",the_redis)
cel=Celery("Tasks", broker=the_redis, backend=the_redis)
#cel=Celery("Tasks",CELERY_BROKER_URL=the_redis)
@cel.task()
def zfunc():
    print("--------------PRINTED FROM IN ZFUNC")
    return 42
#zfunc.apply_async()
#zfunc()
#print("zfunc.delay()------",zfunc.delay())
#Zfunc.delay()
#Zfunc.apply_async()
@cel.task()
def initiLjoV():
  print("tasque File Running initiJoV")
  Rval="return value"
  return Rval
initiLjoV.delay()
run_initiLjoV=initiLjoV.delay()
taskId=run_initiLjoV.task_id
print("taskId.....",taskId)
run_initiLjoV.result.state()
print(run_initiLjoV.result)

#AsyncResult(taskId).ready()
print('ready...',run_initiLjoV.ready())


#AsyncResult(taskId).status()

#run_initiLjoV.state
#run_initiLjoV.status()
#run_initiLjoV.status
#run_initiLjoV.result()
#run_initiLjoV.result


#initiLjoV.delay().state
#initiLjoV.delay().status
#initiLjoV.delay().result


#redis.Redis().client_getname()
#run_initiLjoV=initiLjoV.delay()


"""
print('redis.Redis()',redis.Redis())
print('redis.Redis',redis.Redis)
print('redis',redis)
"""

#print('This is the client id',redis.Redis().client_id)




#print("initiLjoV State 1",run_initiLjoV.state)
#redis.Redis().flushdb()
#print("ended redis")
#print(redis.scan())

#print("initiLjoV State 2",run_initiLjoV.state)
"""
print("initiLjoV State 3",run_initiLjoV.state)
print("initiLjoV State 4",run_initiLjoV.state)
print("initiLjoV State 5",run_initiLjoV.state)
print("initiLjoV State 6",run_initiLjoV.state)
print("initiLjoV State 7",run_initiLjoV.state)
print("initiLjoV State 8",run_initiLjoV.state)
"""
#print("result",run_initiLjoV.result)






