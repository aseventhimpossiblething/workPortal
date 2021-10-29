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
import re
from openpyxl import Workbook
from openpyxl import load_workbook
import xlsxwriter



SheetsFileLocation="/GMDelight/workPortal/Sheets"
currentCommunitiesLocation="/GMDelight/workPortal/Sheets/CommunityUpdates/currentCommunities"
currentGoogleLocation="/GMDelight/workPortal/Sheets/CommunityUpdates/Google/currentGoogle"
currentBingLocation="/GMDelight/workPortal/Sheets/CommunityUpdates/Bing/currentBing"

def ValidatXLSXtime(arr):
        Error=arr+" Generated an error check that filetype is xlsx"
        Valid=arr+" is valid"
        if time.time()-os.path.getctime(arr)>600000:
            print(Error)
        else:
            print(Valid)
        
def rowcheck(Sheet,cols):
     
    Temp=Sheet  
    designated_Columns=cols
    rowCheck=[];
    for cols in designated_Columns:
        colPresent=str(Temp.columns).find(cols);
        if colPresent==-1: 
           rowCheck.append(cols);
    return rowCheck; 

def googConverter(X):
    print("GoogConverter Running")    
    Temp=X;
    cols=Temp.columns
    New_cols=[];
    for col in cols:
        col=str(col).replace("Impr. (Abs. Top) %","Absolute Top Impression Share").replace("Impr. (Top) %","Top Impr. share").replace("New CPC","New Bid").replace("Cost / conv.","CPA").replace("'","").replace('Max. CPC','Bid').replace('Cost','Spend')\
        .replace('Conversions','Conv.').replace('Search top IS','Top Impr. share').replace('Search abs. top IS','Absolute Top Impression Share')\
        .replace('Search impr. share','Impr. share (IS)').replace('Quality Score','Qual. score').replace('Search lost IS (rank)','IS lost to rank')\
        .replace(']','').replace('[','')             
        New_cols.append(col);
    print("Google convert columns ",X.columns) 
    Temp.columns=New_cols
    #print(Temp.columns)    
    print("GoogConverter end")    
    return Temp
      
        


def BidOpFileHandler():
        
    os.chdir('/GMDelight/workPortal/Sheets/BidOpData/MachinePatternSheets/')
    #print('BidOpSeed.xlsx')
    request.files['sheet'].save("Temp.xlsx")
    Temp=pandas.read_excel('Temp.xlsx')
    print("Temp 1")
    print(Temp)
    record_async_start=open("ForestLoadingQueue.txt","w")
    record_async_start.write("This should take no more than 5 min.. else resubmit form")
    record_async_start.close()
      
    target_Variable='New Bid' 
           
    designated_Columns=['Campaign','Ad group','Keyword','Impr.','Match type',target_Variable,'Bid','Clicks','CTR','Avg. CPC','Spend','Conv.','CPA','Conv. rate','Top Impr. share','Absolute Top Impression Share','Impr. share (IS)','Qual. score','IS lost to rank']         
    core_cols=['Campaign','Ad group','Impr.',target_Variable,'Match Number','Market Number','Bid','Clicks','CTR','Avg. CPC','Spend','Conv.','CPA','Conv. rate','Top Impr. share','Absolute Top Impression Share','Impr. share (IS)','Qual. score','IS lost to rank']     
    
    print('target_Variable',target_Variable);
        
    isGoog1=str(Temp.columns).find('Cost')
    isGoog2=str(Temp.columns).find('Conversions')
    Temp=googConverter(Temp)
  
    isTrainingSheet=str(Temp.columns).find('Change'); 
    if isTrainingSheet!=-1:
      
       def TrainingSheetBehavior(x,x2,Temp):
           print('async started')
           #print(x)
           designated_Columns=x
           core_cols=x2   
           Temp=Temp     
           os.chdir('/GMDelight/workPortal/Sheets/BidOpData/MachinePatternSheets/')
                
           rowCheck=rowcheck(Temp,designated_Columns)     
           if len(rowCheck)>0:
                os.chdir('/GMDelight/workPortal/Sheets/BidOpData/MachinePatternSheets/')
                rowCheck=str(rowCheck)
                record_async_start=open("ForestLoadingQueue.txt","w+")
                record_async_start.write(rowCheck)
                record_async_start.close()
                rowCheck=" The following Columns are missing "+rowCheck+" please resubmit sheet "
                return rowCheck
           Temp=pandas.DataFrame(Temp,columns=designated_Columns)
           Temp.fillna(0)
           record_async_start=open("ForestLoadingQueue.txt","w+")
           record_async_start.write("15%")
           record_async_start.close() 
           Temp['Match Number']=BidOpAssist.Match_num(Temp);
                   
           Temp['Market Number']=BidOpAssist.MarketNumberGen(Temp)
           core=pandas.read_excel('BidOpSeed.xlsx')
           core=core.append(Temp, sort='False')
           core=pandas.DataFrame(core,columns=core_cols)     
           core.to_excel("BidOpSeed.xlsx")
                       
           record_async_start=open("ForestLoadingQueue.txt","w")
           record_async_start.write("100%")
           record_async_start.close();  
           
           print("Temp 2")
           print(Temp)
                     
           return "<html><a href='/BasisOfBids'>This Training Sheet will be added to the body of training Data Click to view Basis Sheet</a></html>"
       TrainLoad=threading.Thread(target=TrainingSheetBehavior, args=[designated_Columns, core_cols,Temp]);
       TrainLoad.start(); 
      
       return "<meta http-equiv='Cache-Control' content='no-cache, no-store, must-revalidate'><meta http-equiv='refresh' content='0;URL=/BidOpPending'><html>did not forward</html>"
       
    else:
       print("else path")
       Temp=pandas.DataFrame(Temp,columns=designated_Columns);
       locOfTarg=designated_Columns.index(target_Variable)
       newDesignatedColP1=designated_Columns[:locOfTarg] 
       newDesignatedColP2=designated_Columns[locOfTarg+1:]
       newDesignatedColP=newDesignatedColP1+newDesignatedColP2
       print(designated_Columns)
       print(newDesignatedColP) 
       rowCheck=rowcheck(Temp,newDesignatedColP)     
       print(len(rowCheck)," ",rowCheck); 
       if len(rowCheck)>0:
                os.chdir('/GMDelight/workPortal/Sheets/BidOpData/MachinePatternSheets/')
                rowCheck=str(rowCheck)
                record_async_start=open("ForestLoadingQueue.txt","w+")
                record_async_start.write(rowCheck)
                record_async_start.close()
                rowCheck=" The following Columns are missing "+rowCheck+" please resubmit sheet "
                return rowCheck
              
       print("Just Before threading.thread")
       BidOpAssistAsync=threading.Thread(target=BidOpAssist.BidOpOverview,args=[designated_Columns,core_cols,target_Variable,Temp]);
       BidOpAssistAsync.start(); 
       print("Just After threading.thread")  
       return "<meta http-equiv='Cache-Control' content='no-cache, no-store, must-revalidate'><meta http-equiv='refresh' content='0;URL=/BidOptimisation'><html>did not forward</html>"         
        
    
    toscrn=isTrainingSheet
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
    
    
    if request.files['Communities'].filename.find("xlsx")<1:
                return "The Community Sheet is not XLSX file type";
    if request.files['currentGoogle'].filename.find("xlsx")<1:
                return "The Google Sheet is not XLSX file type";
    if request.files['currentBing'].filename.find("xlsx")<1:
                return "The Bing Sheet is not XLSX file type"; 
     
    os.chdir(currentCommunitiesLocation)
    SHcommand="sudo chmod -R 777 "+currentCommunitiesLocation
    os.system(SHcommand+"/WorkingCommunities")
    request.files['Communities'].save('WorkingCommunities')
        
    os.chdir(currentGoogleLocation)
    request.files['currentGoogle'].save('WorkingGoogle')
    
    os.chdir(currentBingLocation)
    request.files['currentBing'].save('WorkingBing')
     
 
       
    def async_fileloader():
     os.chdir(SheetsFileLocation) 
     storeRequest=open('RequestsVsResponses.txt','w')    
     storeRequest.write("Request, ")
     storeRequest.close()           
     CommunityUpdatesProcess.initialCommUpdatProcess()
    LoadAllCommunityFiles=threading.Thread(target=async_fileloader)
    LoadAllCommunityFiles.start()    

    return "<meta http-equiv='Cache-Control' content='no-cache, no-store, must-revalidate'><meta http-equiv='refresh' content='0;URL=/DisplayCommUpdate'><html>did not forward</html>"     







    

def NCommListFileHandler():
    print("Ncom Starting to Handle Files") 

    print("Prep for reqs--") 
    reqs=request.files,request.files['Communities'],request.files['currentGoogle'],request.files['currentBing'],request.files['Attributes']
    print("Past reqs--") 
    emptyObj="<FileStorage: '' ('application/octet-stream')>" 
    #if emptyObj==str(request.files['currentBing']):
    #     return "Bing slot is empty"
    if emptyObj==str(request.files['currentGoogle']):
        return "Google slot is empty"
    if emptyObj==str(request.files['Communities']):
        return "Active Community slot is empty"
    #if emptyObj==str(request.files['Attributes']):
    #     return "Attributes slot is empty"

    print("Past empty objs---") 
    
    if request.files['Communities'].filename.find("xlsx")<1:
                return "The Community Sheet is not XLSX file type";
    if request.files['currentGoogle'].filename.find("xlsx")<1:
                return "The Google Sheet is not XLSX file type";
    #if request.files['currentBing'].filename.find("xlsx")<1:
    #            return "The Bing Sheet is not XLSX file type"; 
        
    print("Past requests---")  

    os.chdir(currentCommunitiesLocation)
    SHcommand="sudo chmod -R 777 "+currentCommunitiesLocation
    os.system(SHcommand+"/WorkingCommunities")
    request.files['Communities'].save('WorkingCommunities')
        
    os.chdir(currentGoogleLocation)
    request.files['currentGoogle'].save('WorkingGoogle')
    
    os.chdir(currentBingLocation)
    request.files['currentBing'].save('WorkingBing')
     
 
       
    def async_fileloader():
     os.chdir(SheetsFileLocation) 
     storeRequest=open('RequestsVsResponses.txt','w')    
     storeRequest.write("Request, ")
     storeRequest.close()           
     CommunityUpdatesProcess2.initialCommUpdatProcess()
    print("Pre thread fire---")  
    LoadAllCommunityFiles=threading.Thread(target=async_fileloader)
    LoadAllCommunityFiles.start()    

    return "<meta http-equiv='Cache-Control' content='no-cache, no-store, must-revalidate'><meta http-equiv='refresh' content='0;URL=/DisplayCommUpdate2'><html>did not forward</html>"     




    


    

    

