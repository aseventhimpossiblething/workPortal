domain="http://bhiapilink.com"
import CommunityUpdatesProcess
import GetCampaigns
import glob
#import numpy
#import scipy
#import pandas
import BidOpAssist
import fileHandler
import os
from flask import Flask, Markup, render_template, request
from flask import send_file
from flask import send_from_directory
#import get_campaigns
#import expermientCampLabels
#import Campaigns
#import reportexpFreeToDelete
from datetime import datetime
os.system('sudo chmod -R 777 Sheets')
os.system('sudo chmod -R 777 templates')
#from flask_sslify import SSLify

#import psycopg2
app = Flask(__name__,"/static/")
#sslify = SSLify(app)


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











         
@app.route('/get_campaigns')
def official():
    get_campaigns     
    return "."      
       
         

@app.route('/favicon.png')
def favicon():
    return send_from_directory('/app/favicon.png','favicon')     


@app.route('/test')
def testtextfile():
    print("initial directory---------",os.getcwd())
    print("contents of current directory-------------",os.listdir())
    os.chdir("/app/Sheets/CommunityUpdates/Bing/currentBing")
    print("current directory-------------",os.getcwd())
    print("contents of current directory--------------",os.listdir())
    TheSamplefile=open('TheSampleText.txt','r')
   
    j=2+2
    j=str(j)
    return TheSamplefile.read()





@app.route('/DisplayCommUpdate')
def CommUpdateDisplay():
    os.chdir('/var/www/workPortal/Sheets/')     
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
     return "<meta http-equiv='Cache-Control' content='no-cache, no-store, must-revalidate'><meta http-equiv='refresh' content='0;URL=/CommUpdateExcel?'><html>This Message indicates an error in URL Forward</html>"
    if read_storeRequest1!=read_storeRequest2:
     return '<meta http-equiv="refresh" content="120"><html>LOADING..... This can Take up to 10 minuites</html>'



@app.route('/CommUpdateExcel')
def CommUpdateExcel():
 global domain
 domain=domain
 return render_template('/CommUpdateExcel.html',CacheBreakStamp=datetime.now(),domain=domain)

@app.route('/GoogleKWSBMM')
def GoogleKWSBMMKW():
 return send_file("/var/www/workPortal/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleKeywords/GoogleBMMKW/DefaultSheet.xlsx",\
                  attachment_filename="GoogleBMMKW.xlsx")
         
@app.route('/GoogleKWSB')
def GoogleKWSBKW():
 return send_file("/var/www/workPortal/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleKeywords/GoogleBroadKW/DefaultSheet.xlsx",\
                  attachment_filename="GoogleKWSB.xlsx")

@app.route('/GoogleKWSX')
def GoogleKWSX():
 return send_file("/var/www/workPortal/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleKeywords/GoogleExactKW/DefaultSheet.xlsx",\
                  attachment_filename="GoogleKWSX.xlsx")


@app.route('/GoogleAdSBMMA')
def GoogleASBMM():
 return send_file("/var/www/workPortal/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleAds/GoogleAdsVersionA/GoogleAdsVersionABMM/DefaultSheet.xlsx",\
                 attachment_filename="GoogleAdSBMMA.xlsx")
                 
         


@app.route('/GoogleAdSBMMB')
def GoogleBSBMM():
 return send_file("/var/www/workPortal/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleAds/GoogleAdsVersionB/GoogleAdsVersionBBMM/DefaultSheet.xlsx",\
                 attachment_filename="GoogleAdSBMMB.xlsx")
                 
         
  
@app.route('/GoogleAdSBMA')
def GoogleASBM():
 return send_file("/var/www/workPortal/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleAds/GoogleAdsVersionA/GoogleAdsVersionABroad/DefaultSheet.xlsx",\
                 attachment_filename="GoogleAdSBMA.xlsx")
                
         


@app.route('/GoogleAdSBMB')
def GoogleBSBM():
 return send_file("/var/www/workPortal/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleAds/GoogleAdsVersionB/GoogleAdsVersionBBroad/DefaultSheet.xlsx",\
                 attachment_filename="GoogleAdSBMB.xlsx")
                 



@app.route('/GoogleAdSXA')
def GoogleASX():
 return send_file("/var/www/workPortal/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleAds/GoogleAdsVersionA/GoogleAdsVersionAExact/DefaultSheet.xlsx",\
                 attachment_filename="GoogleAdASX.xlsx")
              
         


@app.route('/GoogleAdSXB')
def GoogleBSX():
 return send_file("/var/www/workPortal/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleAds/GoogleAdsVersionB/GoogleAdsVersionBExact/DefaultSheet.xlsx",\
                 attachment_filename="GoogleAdBSX.xlsx")
               
        

@app.route('/BingKWSBMM')
def BingSBMMKW():
 return send_file("/var/www/workPortal/Sheets/CommunityUpdates/Bing/BingOutputs/BingKW/BingKWBMM/DefaultSheet.xlsx",\
                  attachment_filename="BingBMMKW.xlsx")
 
         
@app.route('/BingKWSB')
def BingSBKW():
 return send_file("/var/www/workPortal/Sheets/CommunityUpdates/Bing/BingOutputs/BingKW/BingKWBroad/DefaultSheet.xlsx",\
                  attachment_filename="BingSBKW.xlsx")



@app.route('/BingKWSX')
def BingSXKW():
 return send_file("/var/www/workPortal/Sheets/CommunityUpdates/Bing/BingOutputs/BingKW/BingKWExact/DefaultSheet.xlsx",\
                  attachment_filename="BingSXKW.xlsx")
         

         
       
@app.route('/BingAdSBMMA')
def BingASBMM():
 return send_file("/var/www/workPortal/Sheets/CommunityUpdates/Bing/BingOutputs/BingAds/BingAdsAtype/BingAdsAtypeBMM/DefaultSheet.xlsx",\
                 attachment_filename="BingAdSBMMA.xlsx")
                


@app.route('/BingAdSBMMB')
def BingBSBMM():
 return send_file("/var/www/workPortal/Sheets/CommunityUpdates/Bing/BingOutputs/BingAds/BingAdsBtype/BingAdsBtypeBMM/DefaultSheet.xlsx",\
                 attachment_filename="BingAdSBMMB.xlsx")
              
 
         
         
@app.route('/BingAdSBA')
def BingASB():
 return send_file("/var/www/workPortal/Sheets/CommunityUpdates/Bing/BingOutputs/BingAds/BingAdsAtype/BingAdsAtypeBroad/DefaultSheet.xlsx",\
                 attachment_filename="BingAdSBA.xlsx")
              
         
         
  

@app.route('/BingAdSBB')
def BingBSB():
 return send_file("/var/www/workPortal/Sheets/CommunityUpdates/Bing/BingOutputs/BingAds/BingAdsBtype/BingAdsBtypeBroad/DefaultSheet.xlsx",\
                 attachment_filename="BingAdSBB.xlsx")
                      
                  
 



@app.route('/BingAdSXA')
def BingASX():
 return send_file("/var/www/workPortal/Sheets/CommunityUpdates/Bing/BingOutputs/BingAds/BingAdsAtype/BingAdsAtypeExact/DefaultSheet.xlsx",\
                 attachment_filename="BingAdSXA.xlsx")
                  
         
         
  

@app.route('/BingAdSXB')
def BingBSX():
 return send_file("/var/www/workPortal/Sheets/CommunityUpdates/Bing/BingOutputs/BingAds/BingAdsBtype/BingAdsBtypeExact/DefaultSheet.xlsx",\
                 attachment_filename="BingAdSXB.xlsx")



@app.route('/BasisOfBidsHuman')
def BasisH():
 return send_file('/var/www/workPortal/Sheets/BidOpData/MachinePatternSheets/BidOpSeedViewable.xlsx', attachment_filename='BidOpSeedViewable.xlsx')

         

@app.route('/BasisOfBidsMachine')
def BasisM():
 return send_file('/var/www/workPortal/Sheets/BidOpData/MachinePatternSheets/BidOpSeed.xlsx', attachment_filename='BidOpSeed.xlsx')

         


    










@app.route('/css')
def styleSheet1():
    return render_template('csstemplate.css')

@app.route('/Scripts')
def Scripts():    
    return render_template('Scripts.js')

@app.route('/')
def index():
    global domain     
    domainFavi=domain+"/favicon.png"
    return render_template('LandingTemplate.html',domain=domain,domainFav=domainFavi)

@app.route('/BidOps')
def BidOpInput():
    return render_template('BidOpForm.html')

"""
@app.route('/BidOpTrainingData', methods=['POST','GET'] )
def BidOpTrainingDatas():
    return fileHandler.BidOpFileHandler() 
"""    



@app.route('/BidOPUpload', methods=['POST','GET'])
def BidOPUpload():
    return fileHandler.BidOpFileHandler()



@app.route('/CommunityUpdates')
def CommunitiesUploads():
    return render_template('CommunitiesForm.html')

@app.route('/CommunityFileHander', methods=['POST','GET'])
def CommunityFileHandling():
    return fileHandler.CommListFileHandler()
    

@app.route('/account')
def acc():
    return render_template('account.html')
    
   
@app.route('/BidOpPending')
def acd():
    os.chdir('/var/www/workPortal/Sheets/BidOpData/MachinePatternSheets/')
    readiness=open("ForestLoadingQueue.txt","r")
    ready=readiness.read()
    #if ready=="100%":
    #     BPD="render_template('BidOpPending.html')";
    print(readiness)
    #BPD1="Completed File"  
    BPD='<meta http-equiv="refresh" content="180"><html>This Training Sheet will be added to the body of training Data  - '+ready+"</html>"
    if ready=="100%":
       BPD="render_template('BidOpPending.html')";
    if readiness.find("]")>-1:
       BPD='<meta http-equiv="refresh" content="180"><html>The following columns are missing from the Data set - '+ready+"</html>"           
    #BPD=str(BPD2) 
    print(BPD)
    readiness.close()     
    if ready=="100%":
       return render_template('BidOpPending.html',CacheBreakStamp=datetime.now());
    return BPD







if __name__=='__main__':
    app.run()

