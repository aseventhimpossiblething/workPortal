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
    print("Starting to Handle Files")
    
    """
    if request.files['Communities']:
        print(" asks is comm is present seems to be yes ");
    else:
        print(" asks is comm is present seems to be no ");
      
    if request.files['arandomthing']:
        print(" asks is arandomthing is present seems to be yes ");
    else:
        print(" asks is arandomthing is present seems to be no ");
    """    
        
    simplereq=request.files
    print("Simple request accepted ")
    print("simplereq is =  ",simplereq)
    print("ImmutableMultiDict([('Communities', = ",str(simplereq).find("ImmutableMultiDict([('Communities',"))
    if  str(simplereq).find("ImmutableMultiDict([('Communities',")!=-1:
        print("This is from the Community Sheet")
    else:
        print("Not a communities sheet")
    
    simplereq['communities'].save('WorkingCommunities') 
    print(dir(simplereq))
    #simplereq.save()
     
    #print("simplereq.files['communities']")
    #print(simplereq.files['communities'])     
    print("simplereq.file['communities']")
    print(simplereq.file['communities'])
    print("simplereq['Communities']")     
    #print(simplereq['Communities'])     
    print(simplereq['Communities'])
    print("simplereq['Communities'].filename")
    print(simplereq['Communities'].filename)
    
       
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
            
   

    os.chdir('/app/Sheets/CommunityUpdates/currentCommunities')          
    request.files['Communities'].save('WorkingCommunities')
       
    os.chdir('/app/Sheets/CommunityUpdates/Google/currentGoogle')
    request.files['currentGoogle'].save('WorkingGoogle')
    
    os.chdir('/app/Sheets/CommunityUpdates/Bing/currentBing')
    request.files['currentBing'].save('WorkingBing')
     
    print("saved Files") 
    
        
  
    
   
   
       
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
         







    




    


    

    

