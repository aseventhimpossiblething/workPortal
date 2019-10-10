import CommunityUpdatesProcess
import glob
import numpy
import scipy
import pandas
import BidOpAssist
import fileHandler
import redis
from redis import Redis

from flask import Flask, Markup, render_template, request
from celery import Celery
import os

import psycopg2
from sklearn.ensemble import RandomForestRegressor


#DATABASE_URL = os.environ['DATABASE_URL']


#app = Flask(__name__)   # Flask constructor
#app.config['MAX_CONTENT_LENGTH'] = 1000 * 1024 * 1024

#CommunityUpdatesProcess.initialCommUpdatProcess()




#conn = psycopg2.connect(DATABASE_URL, sslmode='require')
#conn = psycopg2.connect("dbname='dcect276ul8asc' user='ffsezxsqjvacnw' host='ec2-54-83-9-36.compute-1.amazonaws.com' password='657c149f7aac22520e75d72bddb9a16c76e60ac324fb4358f9f579ac1c2619d4'")

#conn.cursor().execute("SELECT * FROM information_schema.tables ")
#conn.cursor().execute("CREATE TABLE newTable (id int,Data text)")

#print("run __: ",conn.cursor().execute("SELECT * FROM dcect276ul8asc"))
#print('run conn.cursor().execute("SELECT * FROM information_schema.tables")___:', conn.cursor().execute("SELECT * FROM information_schema.tables"))
#print(conn.cursor().execute("SELECT * FROM pg_stat_user_tables"))

#print("attempting to create tables")
#conn.cursor().execute("CREATE TABLE DocumentSubmissions("Documents")")
#conn.cursor().execute("CREATE TABLE storage (user_id serial PRIMARY KEY, username VARCHAR (50) UNIQUE NOT NULL, password VARCHAR (50) NOT NULL, email VARCHAR (355) UNIQUE NOT NULL, created_on TIMESTAMP NOT NULL, last_login TIMESTAMP)")

#conn.cursor().close()
#conn.commit()
#print(conn.cursor().execute("SELECT * FROM pg_stat_user_tables"))
#conn.close

#print(conn.cursor().execute("SELECT * FROM pg_stat_user_tables"))
#{{CommonTag}}-{{pagetitle}}
print("*********Celery Code Begin********")


app = Flask(__name__)


print(os.environ['REDIS_URL'])

app.config['CELERY_BROKER_URL'] = os.environ['REDIS_URL']
app.config['CELERY_RESULT_BACKEND'] = os.environ['REDIS_URL']


celery = Celery(app.name, broker=os.environ['REDIS_URL'])
celery.conf.update(app.config)

"""
app.conf.update(BROKER_URL=os.environ['REDIS_URL'],
                CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])
"""                

@celery.task
def spitOut():
    print("this is the print command from inside spitOut")
    return "Spit Out Return String"
   
#spitOut()
#print("attempt to run spitOut")
#print("celery failed")
theCall=spitOut.delay()
#print("spitOut.delay()",spitOut.delay())
#print("spitOut.delay().ready()",spitOut.delay().ready())
print("theCall",theCall)
print("theCall.ready()1",theCall.ready())
print("theCall.state()",theCall.state())
print("theCall.ready()2",theCall.ready())



print("Celery Failing")
#print("spitOut.delay().ready()",spitOut.delay().ready())
#print("spitOut.ready()",spitOut.ready())
#print("spitOut.result()",spitOut.result())
#print(spitOut().delay())
#add.delay(a=2,b=2)
#print("add(8,9).delay()",add(8,9).delay())
#print("add(8,9).ready()",add(8,9).ready())
#print("add(8,9).result()",add(8,9).result())
#print("INDICATE celery Ran Kind of <<No Worker>>!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

@celery.task
def OnPageIterationOfComupdate():
    #CommunityUpdatesProcess.initialCommUpdatProcess()
    #print("-----------------ran OnPageIterationOfComupdate()------------")
    print("++++++ Blank Block ")



print("********Celery Code End*********")

CommonTagAll=Markup('<a href="https://bdx-api-link.herokuapp.com/">BDX Paid Search Portal</a>')

@app.route('/css')
def styleSheet1():
    return render_template('csstemplate.css')

@app.route('/Scripts')
def Scripts():    
    return render_template('Scripts.js')

@app.route('/')
def index():
    indexContent=Markup('<a href="https://www.google.com">"Google"</a><br>\
                 <a href="BidOps">"Bid Ops"</a><br>\
                 <a href="CommunityUpdates">Community Updates</a>')
    return render_template('DefaultTemplate.html',content=indexContent,pagetitle="Paid Search Portal",CommonTag=CommonTagAll)

@app.route('/BidOps')
def BidOpInput():
    return render_template('BidOpForm.html',pagetitle="Bid Optimisation",CommonTag=CommonTagAll)
@app.route('/BidOPUpload', methods=['POST','GET'])
def BidOPUpload():
    return fileHandler.BidOpFileHandler()

@app.route('/CommunityDataFrame')
def CommunityDataFrame():
    print("From Comm Data should be 9*****************************************",add(5,4))
    print("From Comm Data should be 9*****************************************",add(5,4))
    #the functon for col1
    return render_template('CommunityDataframe.html',pagetitle='Community',CommonTag=CommonTagAll,col1="holding")
@app.route('/DataFrameCss')
def DataFrameCss():
    return render_template('DataFrameCss.css')


@app.route('/CommunityUpdates')
def CommunitiesUploads():
    #CommunityUpdatesProcess.initialCommUpdatProcess()
    print("from commudates Form fill out sheet Data should be 8*******************************************",add(5,3))
    print("From Commpdates Form fill out sheet Data should be 8*************************Function of page load*********************",add(5,4))
    return render_template('CommunitiesForm.html',pagetitle="Community Updates",CommonTag=CommonTagAll)
@app.route('/CommunityFileHander', methods=['POST','GET'])
def CommunityFileHandling():
    #CommunityUpdatesProcess.initialCommUpdatProcess()
    print("++++++++++++++++++   filehandler Running   ++++++++++++++++++++++")
    fileHandler.CommListFileHandler()
    
    return OnPageIterationOfComupdate()
    """
    try:
        return fileHandler.CommListFileHandler()
   
    except: 
        return Markup("Files Prohobited")
    """    
   



if __name__=='__main__':
    app.run()

