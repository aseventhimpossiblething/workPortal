import BidOpAssist
import CommunityUpdatesProcess
import CommunityUpdatesProcess2
from datetime import datetime
from flask import Flask, Markup, render_template, request
import glob
import os
import pandas
import time
import xlrd
import io
import threading
from flask import send_file
import gc



SheetsFileLocation="/var/www/workPortal/Sheets"
currentCommunitiesLocation="/var/www/workPortal/Sheets/CommunityUpdates/currentCommunities"
currentGoogleLocation="/var/www/workPortal/Sheets/CommunityUpdates/Google/currentGoogle"
currentBingLocation="/var/www/workPortal/Sheets/CommunityUpdates/Bing/currentBing"

def ValidatXLSXtime(arr):
        Error=arr+" Generated an error check that filetype is xlsx"
        Valid=arr+" is valid"
        if time.time()-os.path.getctime(arr)>600000:
            print(Error)
        else:
            print(Valid)

def BidOpFileHandler():
    #os.chdir('/var/www/workPortal/Sheets')    
    print("********************************BidOpFileHandler() flag 1************************************************")

    #print("request.files______:   ",request.files)

    print("********************************BidOpFileHandler() flag 2************************************************")

    #print("request.files['sheet']______:    ",request.files['sheet'])

    #print("********************************BidOpFileHandler() flag 3*************************************************")

    print("filename    ",request.files['sheet'].filename)
    os.chdir('/var/www/workPortal/Sheets')  
    isTrainSet=request.files['sheet'].filename.lower().find("train") 
    if isTrainSet==-1:
                toscrn="Data Set has not Been Labelled as Training. Bid Optimisation will be attempted"
                request.files['sheet'].save(BidOpTemp)
    if isTrainSet!=-1:  
                toscrn="Dataset is labelled Training. It will Be used as Training Data"
                request.files['sheet'].save(TrainingTemp)
                
    #toscrn=isTrainSet
    print(isTrainSet)
    #os.chdir('/var/www/workPortal/Sheets')   
    #request.files['sheet'].save(TrainingTemp)
        
        

   
    print("*********************************BidOpFileHandler() flag 3***********************************************")

    print("os.getcwd()_____: ",os.getcwd())

    #rint("********************************BidOpFileHandler() flag 5************************************************")

  

    #print("********************************BidOpFileHandler() flag 6************************************************")

    #os.chdir('/var/www/workPortal/Sheets')

    #print("os.chdir(/Sheets)____:")

    #print("********************************BidOpFileHandler() flag 7************************************************")

    #print("os.getcwd()_____: ",os.getcwd())

    #print("********************************BidOpFileHandler() flag 8************************************************")

    #print("os.listdir()____:",os.listdir())

    #print("********************************BidOpFileHandler() flag 9************************************************")
    
    #Decision Must be Made Here Before Save Training or BidOp 
    #request.files['sheet'].save(request.files['sheet'].filename)
        

    #print("********************************BidOpFileHandler() flag 10************************************************")

    #print("os.getcwd()____:",os.getcwd)

    #print("********************************BidOpFileHandler() flag 11************************************************")

    print("os.listdir()____:",os.listdir())

    print("********************************BidOpFileHandler() flag 12************************************************")
    
    # print("os.path.join('/app/Sheets',request.files['sheet'].filename))_____:",os.path.join('/app/Sheets',request.files['sheet'].filename))

    #print("********************************BidOpFileHandler() flag 13************************************************")

    #print("request.files['sheet'].filename_______:     ",request.files['sheet'].filename)

    #print("********************************BidOpFileHandler() flag 14************************************************")

    #print("request.files['sheet']______:    ",request.files['sheet'])

    #print("********************************BidOpFileHandler() flag 15************************************************")

    #print("request.files______:    ",request.files)

    #print("**************************BidOpFileHandler() flag 16******************************************************")
    
    #toscrn = "done"
    #print("**************************BidOpFileHandler() flag 17******************************************************")
    

    
    return toscrn

def CommListFileHandler():
    print("Starting to Handle Files") 
    
    reqs=request.files,request.files['Communities'],request.files['currentGoogle'],request.files['currentBing']   
    emptyObj="<FileStorage: '' ('application/octet-stream')>" 
    if emptyObj==str(request.files['currentBing']):
         return "Bing slot is empty"
    if emptyObj==str(request.files['currentGoogle']):
        return "Google slot is empty"
    if emptyObj==str(request.files['Communities']):
        return "Active Community slot is empty"
       
    
    print("did not Check That File Slots are Filled")    
    
    if request.files['Communities'].filename.find("xlsx")<1:
                return "The Community Sheet is not XLSX file type";
    if request.files['currentGoogle'].filename.find("xlsx")<1:
                return "The Google Sheet is not XLSX file type";
    if request.files['currentBing'].filename.find("xlsx")<1:
                return "The Bing Sheet is not XLSX file type"; 
            
    print("did not Check that Filles are XlSX")    
   
    os.chdir(currentCommunitiesLocation)
    SHcommand="sudo chmod -R 777 "+currentCommunitiesLocation
    os.system(SHcommand+"/WorkingCommunities")
    request.files['Communities'].save('WorkingCommunities')
       
    os.chdir(currentGoogleLocation)
    request.files['currentGoogle'].save('WorkingGoogle')
    
    os.chdir(currentBingLocation)
    request.files['currentBing'].save('WorkingBing')
     
    print("saved Files") 
  
    
   
   
       
    def async_fileloader():
     os.chdir(SheetsFileLocation) 
     storeRequest=open('RequestsVsResponses.txt','w')    
     storeRequest.write("Request, ")
     storeRequest.close()           
     CommunityUpdatesProcess.initialCommUpdatProcess()
    LoadAllCommunityFiles=threading.Thread(target=async_fileloader)
    LoadAllCommunityFiles.start()    
    print("Should respond now!!! ")
    return "<meta http-equiv='Cache-Control' content='no-cache, no-store, must-revalidate'><meta http-equiv='refresh' content='0;URL=http://bhiapilink.com/DisplayCommUpdate'><html>did not forward</html>"
         







    




    


    

    

