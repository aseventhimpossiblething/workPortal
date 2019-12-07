import CommunityUpdatesProcess
import glob
import numpy
import scipy
import pandas
import BidOpAssist
import fileHandler
import redis
import os
import taskque
from celery import Celery

from flask import Flask, Markup, render_template, request


import psycopg2
from sklearn.ensemble import RandomForestRegressor
app = Flask(__name__)

# def print_num_redis_connections():
#     c = redis.Redis(host='redis')
#     print("# of redis clients", len(c.client_list()))

# print_num_redis_connections()


CommonTagAll=Markup('<a href="https://bdx-api-link.herokuapp.com/">BDX Paid Search Portal</a>')

@app.route('/num_of_redis_clients')
def num_redis_clients():
    c = redis.Redis(host='redis', max_connections=1)
    print("# of redis clients", len(c.client_list()))
    return str(len(c.client_list()))

@app.route('/test')
def testasynch():
    from taskque import test
    r = test()
    return str(r)

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
    return render_template('CommunityDataframe.html',pagetitle='Community',CommonTag=CommonTagAll,col1="holding")
@app.route('/DataFrameCss')
def DataFrameCss():
    return render_template('DataFrameCss.css')


@app.route('/CommunityUpdates')
def CommunitiesUploads():
    #CommunityUpdatesProcess.initialCommUpdatProcess()
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
