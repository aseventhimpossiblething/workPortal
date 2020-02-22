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
gc.collect()




def ValidatXLSXtime(arr):
        Error=arr+" Generated an error check that filetype is xlsx"
        Valid=arr+" is valid"
        if time.time()-os.path.getctime(arr)>600000:
            print(Error);
        else:
            print(Valid);

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
    if request.content_length > 6000000:
                print(" File is over 4000kb This is the upload limit -1");
                #return " Cannot Upload as file is over 4000KB ";    
    print("Starting to Handle Files")
    if request.content_length > 6000000:
                #print(" File is over 4000kb This is the upload limit");
                return " Cannot Upload as file is over 4000KB-1 ";
         
     
    simplereq=request.files
    if  str(simplereq).find("ImmutableMultiDict([('Communities',")!=-1:
        floc='/app/Sheets/CommunityUpdates/currentCommunities'
        fnm='Communities'
        savenam='WorkingCommunities'
        nxtStop="The form Load Page"
    if  str(simplereq).find("ImmutableMultiDict([('currentGoogle',")!=-1:
        floc='/app/Sheets/CommunityUpdates/Google/currentGoogle'
        fnm='currentGoogle'
        savenam='WorkingGoogle'
        nxtStop="The bing form Page"
    if  str(simplereq).find("ImmutableMultiDict([('currentBing',")!=-1:
        floc='/app/Sheets/CommunityUpdates/Bing/currentBing'
        fnm='currentBing' 
        savenam='WorkingBing'
        nxtStop="The run wait while we process page and async function"
        
    print("simplereq[fnm].filename = ",simplereq[fnm].filename)
    print("simplereq[fnm].filename.lower() = ",simplereq[fnm].filename.lower()) 
    print("simplereq[fnm].filename.lower().find('xlsx') = ",simplereq[fnm].filename.lower().find("xlsx"))  
    print(simplereq[fnm].filename.lower().find('xlsx')==-1)
    print("___________________________________________________________________________________________________________")
    print("request.content_length = ",request.content_length) 
    #5585833
    if request.content_length > 6000000:
                print(" File is over 4000kb This is the upload limit -2")
                return " Cannot Upload as file is over 4000KB -2 "
    
    #print("len(request.files[fnm].read()) = ",len(request.files[fnm].read())) 
    #print(dir(request)) 
    #print("len(simplereq[fnm]) = " ,len(simplereq[fnm]))    
    
          
    print(simplereq[fnm].filename.lower())
          #print("File Format Needs to be XLSX")
          #return "File format needs to be XLSX"
    
    os.chdir(floc)
    simplereq[fnm].save(savenam)    
    Sheet_Looks=pandas.read_excel(savenam)
    Sheet_Looks=pandas.DataFrame(Sheet_Looks)
    print("Sheet_Looks.iloc[4][1] = ",Sheet_Looks.iloc[4][1])
    print("Sheet_Looks.iloc[4][2] = ",Sheet_Looks.iloc[4][2]) 
    print("Sheet_Looks.iloc[4][3] = ",Sheet_Looks.iloc[4][3])     
    #This is an and and test for Community there should be one for each sheet. 
        
    #str(simplereq).find("ImmutableMultiDict([('Communities',")!=-1    
      
    if Sheet_Looks.iloc[4][3]!='Brand Name' and str(simplereq).find("ImmutableMultiDict([('Communities',")!=-1 and Sheet_Looks.iloc[4][1]!='Builder Name':
        print('This Document is not consistant with the structer of the Community List')
        return 'This Document is not consistant with the structure of the Community List'
    
    #str(simplereq).find("ImmutableMultiDict([('currentGoogle',")!=-1 
       
   
    print("0") 
    print("Sheet_Looks")
    print("1") 
    print(Sheet_Looks)
    print("2")  
    print("Sheet_Looks.iloc[4]")  
    print("3") 
    print(Sheet_Looks.iloc[4]) 
    print("4") 
    print("Sheet_Looks.iloc[4][0]") 
    print("5") 
    print(Sheet_Looks.iloc[4][0])  
    print("6") 
    #print("Sheet_Looks[0] ",Sheet_Looks[0])    

   
    print("7")     
    print(nxtStop) 
    print("8")     
    if fnm=='currentBing':
        print(nxtStop)
        #return(nxtStop)
        def async_fileloader():
          print("async started")           
          os.chdir('/app/Sheets/') 
          storeRequest=open('RequestsVsResponses.txt','w')    
          storeRequest.write("Request, ")
          storeRequest.close()           
          CommunityUpdatesProcess.initialCommUpdatProcess()
        LoadAllCommunityFiles=threading.Thread(target=async_fileloader)
        LoadAllCommunityFiles.start() 
        return "<meta http-equiv='Cache-Control' content='no-cache, no-store, must-revalidate'><meta http-equiv='refresh' content='0;URL=https://communityupdates.herokuapp.com/DisplayCommUpdate'><html>did not forward</html>"
         
    print("9") 
    return "10"




        
        
    
    #else:
    #print("Not a communities sheet")
    
    
    #print("simplereq.files['communities']")
    #print(simplereq.files['communities'])     
    #print("simplereq.file['Communities']")
    #print(simplereq.file['Communities'])
    #print("simplereq['Communities']")     
    #print(simplereq['Communities'])     
    #print(simplereq['Communities'])
    #print("simplereq['Communities'].filename")
    #print(simplereq['Communities'].filename)
    
       
    """
    print(" Check That File Slots are Filled")    
    
    if request.files['Communities'].filename.find("xlsx")<1:
                print("Communities sheet is not XLSX")
                return "The Community Sheet is not XLSX file type";
    if request.files['currentGoogle'].filename.find("xlsx")<1:
                print("Google Sheet is not XLSX")
                return "The Google Sheet is not XLSX file type";
    if request.files['currentBing'].filename.find("xlsx")<1:
                print("Bing Sheet is not XLSX") 
                return "The Bing Sheet is not XLSX file type"; 
    """            
            
   
    """ 
    os.chdir('/app/Sheets/CommunityUpdates/currentCommunities')          
    request.files['Communities'].save('WorkingCommunities')
       
    os.chdir('/app/Sheets/CommunityUpdates/Google/currentGoogle')
    request.files['currentGoogle'].save('WorkingGoogle')
    
    os.chdir('/app/Sheets/CommunityUpdates/Bing/currentBing')
    request.files['currentBing'].save('WorkingBing')
    """
     
    print("saved Files") 
    
        
  
    
   
   
    """   
    def async_fileloader():
     print("async started")           
     os.chdir('/app/Sheets/') 
     storeRequest=open('RequestsVsResponses.txt','w')    
     storeRequest.write("Request, ")
     storeRequest.close()           
     CommunityUpdatesProcess.initialCommUpdatProcess()
    LoadAllCommunityFiles=threading.Thread(target=async_fileloader)
    LoadAllCommunityFiles.start()    
    print("Should respond now!!! ")
    
   
    #return "<html> <a href='https://bdx-api-link.herokuapp.com/test'>WAIT FOR CLEARANCE BEFORE LINK CLICK! OTHERWISE EPIC FAILURE</a></html>" 
    return "<meta http-equiv='Cache-Control' content='no-cache, no-store, must-revalidate'><meta http-equiv='refresh' content='0;URL=https://communityupdates.herokuapp.com/DisplayCommUpdate'><html>did not forward</html>"
    """    







    




    


    

    

