import BidOpAssist
import CommunityUpdatesProcess
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
    print('BidOpSeed.xlsx')
    request.files['sheet'].save("Temp.xlsx")
    Temp=pandas.read_excel('Temp.xlsx')
    #print("os.listdir()")
    #print(os.listdir())
    record_async_start=open("ForestLoadingQueue.txt","w")
    #print("async open and read")    
    #print(record_async_start.read())
    record_async_start.write("5%")
    record_async_start.close()
    record_async_start=open("ForestLoadingQueue.txt","r")
    print(record_async_start.read())    
    record_async_start.close()
    #print(record_async_start.read())     
    

    #designated_Columns=['Campaign','Ad group','Match type','Changes','Bid','Clicks','CTR','Avg. CPC','Spend','Conv.','CPA','Conv. rate','Top Impr. share','Absolute Top Impression Share','Impr. share (IS)','Qual. score','IS lost to rank']     
    #designated_Columns=str(designated_Columns)
    """    
    for cols in designated_Columns:
                       colPresent=str(Temp.columns);
                       colPresent=colPresent.find(cols); 
                       #colPresent=Temp.find(cols);
                       print(colPresent)
                       print("colPresent")
    """                    
    #print("1%")
    #record_async_start.close()    
    #Temp.fillna(0) 
    isTrainingSheet=str(Temp.columns).find('New Bid') 
    if isTrainingSheet!=-1:
       #print(str(Temp['Campaign']).find('MSM')) 
       #Temp.close();
       def TrainBehavior():
           print('async started')
           designated_Columns=['Campaign','Ad group','Match type','Changes','Bid','Clicks','CTR','Avg. CPC','Spend','Conv.','CPA','Conv. rate','Top Impr. share','Absolute Top Impression Share','Impr. share (IS)','Qual. score','IS lost to rank']     
           #if (str(Temp['Campaign']).find('MSM')==-1:
           #    conv_Columns=['Campaign','Ad group','Match type','Changes','Max. CPC','Clicks','CTR','Avg. CPC','Cost','Conversions','Cost / conv.','Conv. rate','Impr. (Top) %','Impr. (Abs. Top) %','Search impr. share','Quality Score','Search lost IS (rank)',]     
           #    Temp.columns=designated_Columns
           """     
           #rowCheck=[];
           #for cols in designated_Columns:
                      #colPresent=Temp.find(cols);
                      #print(colPresent)
                      #print("colPresent") 
                      #if colPresent==-1:
           """                     
                      
           os.chdir('/var/www/workPortal/Sheets/BidOpData/MachinePatternSheets/')
           Temp=pandas.read_excel('Temp.xlsx')
           if (str(Temp['Campaign']).find('MSM'))==-1:
               conv_Columns=['Campaign','Ad group','Match type','Changes','Max. CPC','Clicks','CTR','Avg. CPC','Cost','Conversions','Cost / conv.','Conv. rate','Impr. (Top) %','Impr. (Abs. Top) %','Search impr. share','Quality Score','Search lost IS (rank)',]     
               Temp=pandas.DataFrame(Temp,columns=conv_Columns)
               Temp.columns=designated_Columns 
               print(Temp)
           
           rowCheck=[];
           for cols in designated_Columns:
                       colPresent=str(Temp.columns).find(cols);
                       print(colPresent)
                       print("colPresent") 
                       if colPresent==-1: 
                          rowCheck.append(cols);
           #rowCheck=str(rowCheck)                     
           len(rowCheck);
           print(len(rowCheck)," ",rowCheck); 
           if len(rowCheck)>0:
                return rowCheck;
                
           
           Temp=pandas.DataFrame(Temp,columns=designated_Columns)
           Temp.fillna(0)
           #CoreTrainingData=pandas.read_excel('BidOpSeed.xlsx')
           #CoreTrainingData=CoreTrainingData.append(Temp, sort='False')
           #CoreTrainingData=pandas.DataFrame(CoreTrainingData,columns=['Keyword','New Bid','Campaign','Ad group','Match type','Changes','Bid','Clicks','CTR','Avg. CPC','Spend','Conv.','CPA','Conv. rate','Top Impr. share','Absolute Top Impression Share','Impr. share (IS)','Qual. score','IS lost to rank','IS lost to budget'])
           #CoreTrainingData.to_excel('BidOpSeedViewable.xlsx')
           ccountr=0; 
           record_async_start=open("ForestLoadingQueue.txt","w+")
           record_async_start.write("15%")
           record_async_start.close()     
           Match_Type=[];
           print("Match Type Loop start") 
           for kw in Temp['Match type']:
               kw=kw.lower() 
               #ccountr+=1;
               #kw.lower().find("broad")==>-1:
               #print(kw)
               if kw.find("exact")>-1:
                kw="1";
               if kw.find('broad')>-1:
                kw="2";
               if str(Temp['Campaign'][ccountr]).lower().find("gppc")>-1:
                #print(kw)
                print(type(kw))
                kw=int(kw)
                print(type(kw))
                #print(kw)      
                kw=kw*1000;
               #print("Timeout on second pass count ",ccountr)
               #print(kw)
               Match_Type.append(int(kw))
               #print(len(Match_Type))  
           print("Match type Loop end")
           record_async_start=open("ForestLoadingQueue.txt","w")
           record_async_start.write("25%")
           record_async_start.close()     
               
           Temp['Match Number']=Match_Type;
           #print("-------------------Immediatly following Number conversion below-----")   
           #print("Temp['Match Type']",Temp['Match Type'])     
           #print("-------------------Immediatly following Number conversion above-----")
           #refined_columns='Campaign','Ad group','Match Number','Changes','Bid','Clicks','CTR','Avg. CPC','Spend','Conv.','CPA','Conv. rate','Top Impr. share','Absolute Top Impression Share','Impr. share (IS)','Qual. score','IS lost to rank']     
           #if (str(Temp['Campaign']).find('MSM')==-1:
           #Temp=pandas.DataFrame(Temp,columns=designated_Columns) 
           #print("-------------------Immediatly following Number Reframe Below-----") 
           #print(Temp['Match Type'])
           #print("-------------------Immediatly following reframe above-----") 
           record_async_start=open("ForestLoadingQueue.txt","w")
           record_async_start.write("50%")
           record_async_start.close()     
           Market=[];
          
           TempMarketCount=0;
           print("Newer While Loop Market")     
           while TempMarketCount< len(Temp['Ad group']):
                kw=Temp['Ad group'][TempMarketCount]
                if str(re.search('>\d+',kw)).find("None")!=-1:
                      kw=Temp['Campaign'][TempMarketCount]
                      if str(re.search('>\d+',kw)).find("None")!=-1:  
                         kw="match='>0";
                kw=str(re.search('>\d+',kw))
                targLoc=kw.find("match='>")
                kw=kw[targLoc:].replace("match='>","").replace("'>","")
                Market.append(kw)
                TempMarketCount+=1;
                #print(kw)
           print("Newer While Loop end")      
           Temp['Market Number']=Market
           core=pandas.read_excel('BidOpSeed.xlsx')
           core=core.append(Temp, sort='False')
           core=pandas.DataFrame(core,columns=['Campaign','Ad group','Changes','Match Number','Market Number','Bid','Clicks','CTR','Avg. CPC','Spend','Conv.','CPA','Conv. rate','Top Impr. share','Absolute Top Impression Share','Impr. share (IS)','Qual. score','IS lost to rank'])     
           #if (str(Temp['Campaign']).find('MSM')==-1:) 
           core.to_excel("BidOpSeed.xlsx")
           print(core)
           record_async_start=open("ForestLoadingQueue.txt","w")
           record_async_start.write("100%")
           record_async_start.close();     
           
           return "<html><a href='/BasisOfBids'>This Training Sheet will be added to the body of training Data Click to view Basis Sheet</a></html>"
       #TrainBehavior(Temp);
       TrainLoad=threading.Thread(target=TrainBehavior);
       TrainLoad.start(); 
       #return "Sheet has Been Identified as Training Data it is being formatted and Loaded as such... please wait.. do not press back button"  
       print("is there an attempt to return")
       return "<meta http-equiv='Cache-Control' content='no-cache, no-store, must-revalidate'><meta http-equiv='refresh' content='0;URL=/BidOpPending'><html>did not forward</html>"
       
    else:
       isTrainingSheet="This is Not Training Data, Attempt will be made to Optimise bids"         
                
        
    
    toscrn=isTrainingSheet
    #toscrn="Dataset is labelled Training. It will Be used as Training Data"
                
    #print(isTrainSet)
    print("os.listdir()____:",os.listdir())

    return toscrn
    #return send_file('/var/www/workPortal/Sheets/BidOpData/MachinePatternSheets/BidOpSeed.xlsx', attachment_filename='BidOpSeed.xlsx')

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
    #return "<meta http-equiv='Cache-Control' content='no-cache, no-store, must-revalidate'><meta http-equiv='refresh' content='0;URL=http://bhiapilink.com/DisplayCommUpdate'><html>did not forward</html>"
    return "<meta http-equiv='Cache-Control' content='no-cache, no-store, must-revalidate'><meta http-equiv='refresh' content='0;URL=/DisplayCommUpdate'><html>did not forward</html>"     







    




    


    

    

