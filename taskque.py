"""
Need to determine state/status
Need to limit redis/celery connections
reliable redis/celery cmds
voir les log persistant
Separer les contenue static es dynamique
"""
print("this is the master branch tasque..............................................................")


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
the_redis=os.environ.get("REDIS_URL")
#cel=Celery("taskque", broker=the_redis)
from huey import RedisHuey
huey = RedisHuey('taskque')
#cel=huey("taskque", broker=the_redis)

@huey.task
def huey_Zfunc():
    print("Huey_ huey_Zfunc()........................what worker? ")
huey_Zfunc.periodic_task()    
"""
@cel.task()
def zfunc():
    print("--------------PRINTED FROM IN ZFUNC")

@cel.task()
def initiLjoV():
  print("tasque File Running initiJoV")
  Rval="return value"
  return Rval
@cel.task()
def pfunk(x,y):
    print(x)
    print(y)

@cel.task()
def borrowedCelery():
    print("should be run on celery Borrowed Celey from task to communities!!!!!!!!!!!!!!!!!!!!!!!!")


@cel.task()
def cel_save():
    print("cel_save.... run")
    print("from cel ...fileHandler ")
    print(fileHandler.request.files['currentGoogle'])
    print(fileHandler.request.files['currentBing'])
    
    os.chdir('/app/Sheets/CommunityUpdates/Google/currentGoogle')
    fileHandler.request.files['currentGoogle'].save('WorkingGoogle')
    
    os.chdir('/app/Sheets/CommunityUpdates/Bing/currentBing')
    fileHandler.request.files['currentBing'].save('WorkingBing')

@cel.task()
def FileAsynchLoad(filename,fileLocation):
    print("..................FileAsynchLoad(file,filename)...................................................")
    print('input filename',filename )
    print('input fileLocation',fileLocation)
    print('os.chdir(fileLocation)')
    os.chdir(fileLocation)
    print("os.listdir()")
    print(os.listdir())
    #print(fileLocation)
    #file=pandas.read_excel(filename)
    #print(filename)
    #print(file)
    #return file
  """
    

    









