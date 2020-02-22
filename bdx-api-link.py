import CommunityUpdatesProcess
import fileHandler
import os
from flask import Flask, Markup, render_template, request
from flask import send_file
from flask import send_from_directory
from datetime import datetime




app = Flask(__name__,"/static/")


@app.route('/testofjs')
def tstfjs():
 return render_template('testofjs.html')






@app.route('/favicon.png')
def favicon():
    return send_from_directory('/app/favicon.png','favicon')     



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
     return "<meta http-equiv='Cache-Control' content='no-cache, no-store, must-revalidate'><meta http-equiv='refresh' content='0;URL=https://communityupdates.herokuapp.com/CommUpdateExcel?'><html>This Message indicates an error in URL Forward</html>"
    if read_storeRequest1!=read_storeRequest2:
     return '<meta http-equiv="refresh" content="120"><html>LOADING..... This can Take up to 10 minuites</html>'



@app.route('/CommUpdateExcel')
def CommUpdateExcel():
 return render_template('CommUpdateExcel.html',CacheBreakStamp=datetime.now())

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
 return send_file("/app/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleAds/GoogleAdsVersionA/GoogleAdsVersionABMM/DefaultSheet.xlsx",\
                 attachment_filename="GoogleAdSBMMA.xlsx")
                 
         


@app.route('/GoogleAdSBMMB')
def GoogleBSBMM():
 return send_file("/app/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleAds/GoogleAdsVersionB/GoogleAdsVersionBBMM/DefaultSheet.xlsx",\
                 attachment_filename="GoogleAdSBMMB.xlsx")
                 
         
  
@app.route('/GoogleAdSBMA')
def GoogleASBM():
 return send_file("/app/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleAds/GoogleAdsVersionA/GoogleAdsVersionABroad/DefaultSheet.xlsx",\
                 attachment_filename="GoogleAdSBMA.xlsx")
                
         


@app.route('/GoogleAdSBMB')
def GoogleBSBM():
 return send_file("/app/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleAds/GoogleAdsVersionB/GoogleAdsVersionBBroad/DefaultSheet.xlsx",\
                 attachment_filename="GoogleAdSBMB.xlsx")
                 



@app.route('/GoogleAdSXA')
def GoogleASX():
 return send_file("/app/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleAds/GoogleAdsVersionA/GoogleAdsVersionAExact/DefaultSheet.xlsx",\
                 attachment_filename="GoogleAdASX.xlsx")
              
         


@app.route('/GoogleAdSXB')
def GoogleBSX():
 return send_file("/app/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleAds/GoogleAdsVersionB/GoogleAdsVersionBExact/DefaultSheet.xlsx",\
                 attachment_filename="GoogleAdBSX.xlsx")
               

         

         
         
         

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
         
         

         
       
@app.route('/BingAdSBMMA')
def BingASBMM():
 return send_file("/app/Sheets/CommunityUpdates/Bing/BingOutputs/BingAds/BingAdsAtype/BingAdsAtypeBMM/DefaultSheet.xlsx",\
                 attachment_filename="BingAdSBMMA.xlsx")
                


@app.route('/BingAdSBMMB')
def BingBSBMM():
 return send_file("/app/Sheets/CommunityUpdates/Bing/BingOutputs/BingAds/BingAdsBtype/BingAdsBtypeBMM/DefaultSheet.xlsx",\
                 attachment_filename="BingAdSBMMB.xlsx")
              
         
         
         
         
         
         
@app.route('/BingAdSBA')
def BingASB():
 return send_file("/app/Sheets/CommunityUpdates/Bing/BingOutputs/BingAds/BingAdsAtype/BingAdsAtypeBroad/DefaultSheet.xlsx",\
                 attachment_filename="BingAdSBA.xlsx")
              
         
         
  

@app.route('/BingAdSBB')
def BingBSB():
 return send_file("/app/Sheets/CommunityUpdates/Bing/BingOutputs/BingAds/BingAdsBtype/BingAdsBtypeBroad/DefaultSheet.xlsx",\
                 attachment_filename="BingAdSBB.xlsx")
                      
                  
 



@app.route('/BingAdSXA')
def BingASX():
 return send_file("/app/Sheets/CommunityUpdates/Bing/BingOutputs/BingAds/BingAdsAtype/BingAdsAtypeExact/DefaultSheet.xlsx",\
                 attachment_filename="BingAdSXA.xlsx")
                  
         
         
  

@app.route('/BingAdSXB')
def BingBSX():
 return send_file("/app/Sheets/CommunityUpdates/Bing/BingOutputs/BingAds/BingAdsBtype/BingAdsBtypeExact/DefaultSheet.xlsx",\
                 attachment_filename="BingAdSXB.xlsx")
                 

         



    










@app.route('/css')
def styleSheet1():
    return render_template('csstemplate.css')

@app.route('/Scripts')
def Scripts():    
    return render_template('Scripts.js')

@app.route('/')
def index():
    domainName="https://bdxapilink.com"
    domainCSS0="https://bdxapilink.com/css"
    domainFavi="https://bdxapilink.com/favicon.png"
    return render_template('LandingTemplate.html',domain=domainName,domainFav=domainFavi,domainCSS=domainCSS0)


@app.route('/CommunityDataFrame')
def CommunityDataFrame():
    return render_template('CommunityDataframe.html',pagetitle='Community',CommonTag=CommonTagAll,col1="holding")
@app.route('/DataFrameCss')
def DataFrameCss():
    return render_template('DataFrameCss.css')

@app.route('/CommunityUpdates')
def CommunitiesUploads():
    #return render_template('CommunitiesForm.html')
    return render_template('CommflowForm1.html')
#/ComFlow1

@app.route('/CommunityFileHander', methods=['POST','GET'])
def CommunityFileHandling():
    return fileHandler.CommListFileHandler()




@app.route('/ComFlow1')
def Commumflow1():
    return render_template('CommflowForm1.html')
#CommflowForm1.html
    
   
   



if __name__=='__main__':
    app.run()

