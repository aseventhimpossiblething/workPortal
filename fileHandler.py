import BidOpAssist
import CommunityUpdatesProcess
from datetime import datetime
from flask import Flask, Markup, render_template, request
import glob
import os
import psycopg2
import pandas
import time
import xlrd
import io
#import taskque
import threading
from flask import send_file




def ValidatXLSXtime(arr):
        Error=arr+" Generated an error check that filetype is xlsx"
        Valid=arr+" is valid"
        if time.time()-os.path.getctime(arr)>600000:
            print(Error)
        else:
            print(Valid)

def BidOpFileHandler():
    print("********************************BidOpFileHandler() flag 1************************************************")

    print("request.files______:   ",request.files)

    print("********************************BidOpFileHandler() flag 2************************************************")

    print("request.files['sheet']______:    ",request.files['sheet'])

    print("********************************BidOpFileHandler() flag 3*************************************************")

    print("request.files['sheet'].filename_______:     ",request.files['sheet'].filename)

   
    print("*********************************BidOpFileHandler() flag 4***********************************************")

    print("os.getcwd()_____: ",os.getcwd())

    print("********************************BidOpFileHandler() flag 5************************************************")

    print("os.listdir()____:",os.listdir())

    print("********************************BidOpFileHandler() flag 6************************************************")

    os.chdir('/app/Sheets')

    print("os.chdir(/Sheets)____:")

    print("********************************BidOpFileHandler() flag 7************************************************")

    print("os.getcwd()_____: ",os.getcwd())

    print("********************************BidOpFileHandler() flag 8************************************************")

    print("os.listdir()____:",os.listdir())

    print("********************************BidOpFileHandler() flag 9************************************************")

    request.files['sheet'].save(request.files['sheet'].filename)

    print("********************************BidOpFileHandler() flag 10************************************************")

    print("os.getcwd()____:",os.getcwd)

    print("********************************BidOpFileHandler() flag 11************************************************")

    print("os.listdir()____:",os.listdir())

    print("********************************BidOpFileHandler() flag 12************************************************")
    
    print("os.path.join('/app/Sheets',request.files['sheet'].filename))_____:",os.path.join('/app/Sheets',request.files['sheet'].filename))

    print("********************************BidOpFileHandler() flag 13************************************************")

    print("request.files['sheet'].filename_______:     ",request.files['sheet'].filename)

    print("********************************BidOpFileHandler() flag 14************************************************")

    print("request.files['sheet']______:    ",request.files['sheet'])

    print("********************************BidOpFileHandler() flag 15************************************************")

    print("request.files______:    ",request.files)

    print("**************************BidOpFileHandler() flag 16******************************************************")
    
    toscrn = "done"
    print("**************************BidOpFileHandler() flag 17******************************************************")
    

    
    return toscrn

def CommListFileHandler():
    
      
        
    reqs=request.files,request.files['Communities'],request.files['currentGoogle'],request.files['currentBing']   
    emptyObj="<FileStorage: '' ('application/octet-stream')>" 
    if emptyObj==str(request.files['currentBing']):
         return "Bing slot is empty"
    if emptyObj==str(request.files['currentGoogle']):
        return "Google slot is empty"
    if emptyObj==str(request.files['Communities']):
        return "Active Community slot is empty"

    if request.files['Communities'].filename.find("xlsx")<1:
                return "The Community Sheet is not XLSX file type";
    if request.files['currentGoogle'].filename.find("xlsx")<1:
                return "The Google Sheet is not XLSX file type";
    if request.files['currentBing'].filename.find("xlsx")<1:
                return "The Bing Sheet is not XLSX file type";       
   
    os.chdir('/app/Sheets/CommunityUpdates/currentCommunities')          
    request.files['Communities'].save('WorkingCommunities')
       
    os.chdir('/app/Sheets/CommunityUpdates/Google/currentGoogle')
    request.files['currentGoogle'].save('WorkingGoogle')
    
    os.chdir('/app/Sheets/CommunityUpdates/Bing/currentBing')
    request.files['currentBing'].save('WorkingBing')
     
    
      
    def async_fileloader():       
     CommunityUpdatesProcess.initialCommUpdatProcess()
    LoadAllCommunityFiles=threading.Thread(target=async_fileloader)
    LoadAllCommunityFiles.start()    
    
    
        
    HTMLoutput="This will be 3 modules  Modules as follows  Module 1: 3 links to the Community, Google, and Bing upload outputs Module 2:Google Outputs link1, Google KWs all match types. Link 2 google Adds Ad Types A+b and all Match types "    
    toscrn = HTMLoutput
    return send_file("/app/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleKeywords/GoogleBMMKW/911cor.xlsx", attachment_filename="911cor.xlsx")
    """
    return "<html><a href="/app/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleKeywords/GoogleBMMKW/DefaultSheet.xlsx" target="_blank">\
    <p>At Q Attempt Download</p></a><br><a href='https://bdx-api-link.herokuapp.com/test'>\
    WAIT FOR CLEARANCE BEFORE LINK CLICK! OTHERWISE EPIC FAILURE</a></html>" 
    """
         







    




    


    

    

