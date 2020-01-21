import CommunityUpdatesProcess
import glob
import numpy
import scipy
import pandas
import BidOpAssist
import fileHandler
import redis
import os
from flask import Flask, Markup, render_template, request
from celery import Celery
from flask import send_file
#import taskque
from datetime import date
print("TODAYS DATE!!_________________",date.today())
         


import psycopg2
from sklearn.ensemble import RandomForestRegressor
app = Flask(__name__)


#DATABASE_URL = os.environ['DATABASE_URL']


#application = Flask(__name__)   # Flask constructor
#app.config['MAX_CONTENT_LENGTH'] = 1000 * 1024 * 1024



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







#print(" start of index CommunityUpdatesProcess.IsCommUpdateRunning ",CommunityUpdatesProcess.IsCommUpdateRunning)

CommonTagAll=Markup('<a href="https://bdx-api-link.herokuapp.com/">BDX Paid Search Portal</a>')

@app.route('/test')
def testtextfile():
    print("initial directory---------",os.getcwd())
    print("contents of current directory-------------",os.listdir())
    #os.chdir("/app/Sheets/CommunityUpdates")
    os.chdir("/app/Sheets/CommunityUpdates/Bing/currentBing")
    print("current directory-------------",os.getcwd())
    print("contents of current directory--------------",os.listdir())
    TheSamplefile=open('TheSampleText.txt','r')
    #TheSamplefile=open('TheSampleText.txt','w+') 
    #print(TheSamplefile.read())     
    #print(os.getcwd())
     
    j=2+2
    j=str(j)
    return TheSamplefile.read()



@app.route('/DisplayCommUpdate')
def CommUpdateDisplay():
    os.chdir('/app/Sheets/')     
    storeRequest=open('RequestsVsResponses.txt','r+')
    read_storeRequest=storeRequest.read()
    storeRequest.close()
    print("read_storeRequest ",read_storeRequest)
    read_storeRequest1=read_storeRequest.count('Request')
    read_storeRequest2=read_storeRequest.count('Response')
    print(read_storeRequest1," <> ",read_storeRequest)     
    print("read_storeRequest ",read_storeRequest)     
    print("________________________________________________________________exp ",read_storeRequest1," : ",read_storeRequest2)
    if read_storeRequest1==read_storeRequest2:
     return "<meta http-equiv='Cache-Control' content='no-cache, no-store, must-revalidate'><meta http-equiv='refresh' content='0;URL=https://bdx-api-link.herokuapp.com/CommUpdateExcel?'><html>This Message indicates an error in URL Forward</html>"
     #return "Alt Message Test"
     #return "<meta http-equiv='refresh' content='0;URL=https://www.google.com'><html>Should forward to google</html>"
    if read_storeRequest1!=read_storeRequest2:
     return '<meta http-equiv="refresh" content="120"><html>LOADING..... This can Take up to 10 minuites </html>'


#'0;URL=https://bdx-api-link.herokuapp.com/DisplayCommUpdate'
#https://bdx-api-link.herokuapp.com/GoogleKWSBMM
@app.route('/CommUpdateExcel')
def CommUpdateExcel():
 return render_template('CommUpdateExcel.html')

@app.route('/GoogleKWSBMM')
def GoogleKWSBMMKW():
 return send_file("/app/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleKeywords/GoogleBMMKW/DefaultSheet.xlsx",\
                  attachment_filename="GoogleBMMKW.xlsx")
         
@app.route('/GoogleKWSB')
def GoogleKWSBKW():
 return send_file("/app/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleKeywords/GoogleBroadKW/DefaultSheet.xlsx",\
                  attachment_filename="GoogleKWSB.xlsx")

@app.route('/GoogleKWSX')
def GoogleKWSX():
 return send_file("/app/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleKeywords/GoogleExactKW/DefaultSheet.xlsx",\
                  attachment_filename="GoogleKWSX.xlsx")


@app.route('/GoogleAdSBMMA')
def GoogleASBMM():
 #print(date.today())        
 #TodaysDate="EL-Dia-De-Hoy"+str(date.today())+".xlsx"        
 return send_file("/app/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleAds/GoogleAdsVersionA/GoogleAdsVersionABMM/DefaultSheet.xlsx",\
                 attachment_filename="GoogleAdSBMMA.xlsx")
                 #attachment_filename=TodaysDate) 
         


@app.route('/GoogleAdSBMMB')
def GoogleBSBMM():
 #print(date.today())        
 #TodaysDate="EL-Dia-De-Hoy"+str(date.today())+".xlsx"        
 return send_file("/app/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleAds/GoogleAdsVersionB/GoogleAdsVersionBBMM/DefaultSheet.xlsx",\
                 attachment_filename="GoogleAdSBMMB.xlsx")
                 #attachment_filename=TodaysDate)
         
  
@app.route('/GoogleAdSBMA')
def GoogleASBMM():
 #print(date.today())        
 #TodaysDate="EL-Dia-De-Hoy"+str(date.today())+".xlsx"        
 return send_file("/app/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleAds/GoogleAdsVersionA/GoogleAdsVersionABM/DefaultSheet.xlsx",\
                 attachment_filename="GoogleAdSBMMA.xlsx")
                 #attachment_filename=TodaysDate) 
         


@app.route('/GoogleAdSBMB')
def GoogleBSBMM():
 #print(date.today())        
 #TodaysDate="EL-Dia-De-Hoy"+str(date.today())+".xlsx"        
 return send_file("/app/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleAds/GoogleAdsVersionB/GoogleAdsVersionBBM/DefaultSheet.xlsx",\
                 attachment_filename="GoogleAdSBMMB.xlsx")
                 #attachment_filename=TodaysDate)  






@app.route('/BingKWSBMM')
def BingSBMMKW():
 return send_file("/app/Sheets/CommunityUpdates/Bing/BingOutputs/BingKW/BingKWBMM/DefaultSheet.xlsx",\
                  attachment_filename="BingBMMKW.xlsx")
 
         
@app.route('/BingKWSB')
def BingSBKW():
 return send_file("/app/Sheets/CommunityUpdates/Bing/BingOutputs/BingKW/BingKWBroad/DefaultSheet.xlsx",\
                  attachment_filename="BingSBKW.xlsx")



@app.route('/BingKWSX')
def BingSXKW():
 return send_file("/app/Sheets/CommunityUpdates/Bing/BingOutputs/BingKW/BingKWExact/DefaultSheet.xlsx",\
                  attachment_filename="BingSXKW.xlsx")
         

         
       

                  

         


         



"""
@app.route('/dnlde')
def dnld():
    return send_file("/app/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleKeywords/GoogleBMMKW/911cor.xlsx", attachment_filename="911cor.xlsx")     
"""         
         
    










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
    #print("++++++++++++++++++   filehandler Running   ++++++++++++++++++++++")
    #fileHandler.CommListFileHandler()
    
    return fileHandler.CommListFileHandler()
    
    #return '<html><p>empty</p></html>'
    """
    try:
        return fileHandler.CommListFileHandler()
   
    except: 
        return Markup("Files Prohobited")
    """    
   



if __name__=='__main__':
    app.run()

