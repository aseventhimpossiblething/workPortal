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
from openpyxl import Workbook
from openpyxl import load_workbook
import xlsxwriter


#os.system('echo his is Echoed by system os number 1')
SheetsFileLocation="/var/www/workPortal/Sheets"
currentCommunitiesLocation="/var/www/workPortal/Sheets/CommunityUpdates/currentCommunities"
currentGoogleLocation="/var/www/workPortal/Sheets/CommunityUpdates/Google/currentGoogle"
currentBingLocation="/var/www/workPortal/Sheets/CommunityUpdates/Bing/currentBing"
#os.system('echo his is Echoed by system os number 2')
def ValidatXLSXtime(arr):
        Error=arr+" Generated an error check that filetype is xlsx"
        Valid=arr+" is valid"
        if time.time()-os.path.getctime(arr)>600000:
            print(Error)
        else:
            print(Valid)

def BidOpFileHandler():
        
    os.chdir('/var/www/workPortal/Sheets/BidOpData/MachinePatternSheets/')
    request.files['sheet'].save("Temp")
    Temp=pandas.read_excel('Temp')
    isTrainingSheet=str(Temp.columns).find('New Bid') 
    if isTrainingSheet!=-1:
       os.chdir('/var/www/workPortal/Sheets/BidOpData/MachinePatternSheets/')
       Temp=pandas.DataFrame(Temp,columns=['Campaign','Ad group','Keyword','Match type','Changes','New Bid','Bid','Clicks','CTR','Avg. CPC','Spend','Conv.','CPA','Conv. rate','Top Impr. share','Absolute Top Impression Share','Impr. share (IS)','Qual. score','IS lost to rank','IS lost to budget'])
       CoreTrainingData=pandas.read_excel('BidOpSeed.xlsx')
       print("----------------------------------Temp------------------------")
       print(Temp)
       print('--------------------------Core Training Data------------------')
       print(CoreTrainingData)
       print("_________________________________________________________________________________________") 
       print("_________________________________________________________________________________________") 
       CoreTrainingData=CoreTrainingData.append(Temp, sort='False')
       print("_________________________________________________________________________________________") 
       print("_________________________________________________________________________________________") 
       print("--------------------------Merged New Core Data-------------------------") 
       print(CoreTrainingData)
       #writer=pandas.excelWriter('DefaultSheet.xlsx').to_excel()
       CoreTrainingData.to_excel('BidOpSeed.xlsx')
       #.to_excel(writer)
       isTrainingSheet='This Training Sheet will be added to the body of training Data'
    else:
        isTrainingSheet="This is Not Training Data, Attempt will be made to Optimise bids"         
                
        
    
    toscrn=isTrainingSheet
    #toscrn="Dataset is labelled Training. It will Be used as Training Data"
                
    #print(isTrainSet)
    print("os.listdir()____:",os.listdir())

    #return toscrn
    return send_file('/var/www/workPortal/Sheets/BidOpData/MachinePatternSheets/BidOpSeed.xlsx', attachment_filename='BidOpSeed.xlsx')

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
       
    
    #print("did not Check That File Slots are Filled")    
    
    if request.files['Communities'].filename.find("xlsx")<1:
                return "The Community Sheet is not XLSX file type";
    if request.files['currentGoogle'].filename.find("xlsx")<1:
                return "The Google Sheet is not XLSX file type";
    if request.files['currentBing'].filename.find("xlsx")<1:
                return "The Bing Sheet is not XLSX file type"; 
            
    #print("did not Check that Filles are XlSX")    
   
    os.chdir(currentCommunitiesLocation)
    SHcommand="sudo chmod -R 777 "+currentCommunitiesLocation
    os.system(SHcommand+"/WorkingCommunities")
    request.files['Communities'].save('WorkingCommunities')
       
    os.chdir(currentGoogleLocation)
    request.files['currentGoogle'].save('WorkingGoogle')
    
    os.chdir(currentBingLocation)
    request.files['currentBing'].save('WorkingBing')
     
    #print("saved Files") 
  
    
   
   
       
    def async_fileloader():
     os.chdir(SheetsFileLocation) 
     storeRequest=open('RequestsVsResponses.txt','w')    
     storeRequest.write("Request, ")
     storeRequest.close()           
     CommunityUpdatesProcess.initialCommUpdatProcess()
    LoadAllCommunityFiles=threading.Thread(target=async_fileloader)
    LoadAllCommunityFiles.start()    
    #print("Should respond now!!! ")
    #os.system('echo his is Echoed by system os number 3')    
    return "<meta http-equiv='Cache-Control' content='no-cache, no-store, must-revalidate'><meta http-equiv='refresh' content='0;URL=http://bhiapilink.com/DisplayCommUpdate'><html>did not forward</html>"
         







    




    


    

    

