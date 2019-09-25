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

def ValidatXLSXtime(arr):
        #print("Crtitical Value ",time.time()-os.path.getctime(arr))
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
    reqs=request.files,request.files['currentGoogle'],request.files['currentGoogle'],request.files['currentBing']   
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
   
    #newDate=str(datetime.today()).replace("-","")
        
    request.files['Communities'].save('WorkingCommunities')
    print("after first save")
    
    os.chdir('/app/Sheets/CommunityUpdates/Google/currentGoogle')
    request.files['currentGoogle'].save('WorkingGoogle')
    
    os.chdir('/app/Sheets/CommunityUpdates/Bing/currentBing')
    request.files['currentBing'].save('WorkingBing')
                            
    os.chdir('/app/Sheets/CommunityUpdates/currentCommunities')
    recent=max(glob.glob('*.xlsx'), key=os.path.getctime)
    ValidatXLSXtime(recent)
        
    os.chdir('/app/Sheets/CommunityUpdates/Google/currentGoogle')
    recent=max(glob.glob('*.xlsx'), key=os.path.getctime)
    ValidatXLSXtime(recent)
        
    os.chdir('/app/Sheets/CommunityUpdates/Bing/currentBing')
    recent=max(glob.glob('*.xlsx'), key=os.path.getctime)
    ValidatXLSXtime(recent)
           
    CommunityUpdatesProcess.initialCommUpdatProcess() 
    print(CommunityUpdatesProcess.initialCommUpdatProcess())    
    HTMLoutput=Markup(CommunityUpdatesProcess.initialCommUpdatProcess())
    print(CommunityUpdatesProcess.ommunityColTitles)
    print(CommunityUpdatesProcess.CommunityRow1) 
    print(CommunityUpdatesProcess.CommunityRow2)
    print(CommunityUpdatesProcess.CommunityRow4)

    toscrn = HTMLoutput
        
    return toscrn


    




    


    

    

