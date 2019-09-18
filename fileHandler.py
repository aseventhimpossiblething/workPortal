import BidOpAssist
from flask import Flask, Markup, render_template, request
import glob
import os
import psycopg2
import pandas
import xlrd
import io

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
    
    print("********************************CommListFileHandler() flag 2************************************************")

    print("request.files['Communities']______:    ",request.files['Communities'])
    print("request.files['currentGoogle']______:    ",request.files['currentGoogle'])
    print("request.files['currentBing']______:    ",request.files['currentBing'])

    print("********************************CommListFileHandler() flag 3*************************************************")

    #print("request.files['Communities'].filename_______:     ",request.files['Communities'].filename)
    #request.files['Communities'].filename.index('xlsx')
    #print("request.files['Communities'].filename.index('xlsx')",request.files['Communities'].filename.index('xlsx'))
    #print("type and index('int')",type(request.files['Communities'].filename.index('xlsx')).index('int'))
    
    
    """
    if request.files['Communities'].filename.index('xlsx')=="<class 'int'>":
       print("normal")
    if type(request.files['Communities'].filename.index('xlsx'))!="<class 'int'>":
       print("The File Entered as Community is not in the xlsx Filetype")
       return "The File Entered as Community List is not in the xlsx Filetype"
    if type(request.files['currentGoogle'].filename.index('xlsx'))!="<class 'int'>":
       print("The File Entered as Active Google List is not in the xlsx Filetype")
       return "The File Entered as Active Google List is not in the xlsx Filetype"
    if type(request.files['currentBing'].filename.index('xlsx'))!="<class 'int'>":
       print("The File Entered as Active Bing List is not in the xlsx Filetype")
       return "The File Entered as Active Bing List is not in the xlsx Filetype"
   """    
    
    print(request.files['Communities'].filename.index('xlsx'))
    print("6",type(6))
    if <class 'int'>==type(3):
        print("<class 'int'>==type(3)")
    else:
        print("<class 'int'>==type(3)")
    
    
    #print("request.files['currentGoogle'].filename_______:     ",request.files['currentGoogle'].filename)
    #print("request.files['currentBing'].filename_______:     ",request.files['currentBing'].filename)



    print("*********************************CommListFileHandler() flag 4***********************************************")
    os.chdir('/app/Sheets/CommunityUpdates/currentCommunities')
    print("os.getcwd()_____: ",os.getcwd())
    request.files['Communities'].save(request.files['Communities'].filename)
    
    os.chdir('/app/Sheets/CommunityUpdates/Google/currentGoogle')
    print("os.getcwd()_____: ",os.getcwd())
    request.files['currentGoogle'].save(request.files['currentGoogle'].filename)
    
    os.chdir('/app/Sheets/CommunityUpdates/Bing/currentBing')
    print("os.getcwd()_____: ",os.getcwd())
    request.files['currentBing'].save(request.files['currentBing'].filename)

  
                                                   
    print("********************************CommListFileHandler() flag 5************************************************")
    os.chdir('/app/Sheets/CommunityUpdates/currentCommunities')
    print("os.listdir()____:",os.listdir())
    
    os.chdir('/app/Sheets/CommunityUpdates/Google/currentGoogle')
    print("os.listdir()____:",os.listdir())
    
    os.chdir('/app/Sheets/CommunityUpdates/Bing/currentBing')
    print("os.listdir()____:",os.listdir())
    
    

    print("********************************CommListFileHandler() flag 6************************************************")
    os.chdir('/app/Sheets/CommunityUpdates/currentCommunities')
    recent=max(glob.glob('*'), key=os.path.getctime)
    print("recent____",recent)
    print("os.listdir()____:",os.listdir())
    
    
    os.chdir('/app/Sheets/CommunityUpdates/Google/currentGoogle')
    recent=max(glob.glob('*'), key=os.path.getctime)
    print("recent____",recent)
    print("os.listdir()____:",os.listdir())
    
    os.chdir('/app/Sheets/CommunityUpdates/Bing/currentBing')
    recent=max(glob.glob('*'), key=os.path.getctime)
    print("recent____",recent)
    print("os.listdir()____:",os.listdir())

   
    print("********************************CommListFileHandler() flag 11************************************************")
    
    
    #print("os.listdir()____:",os.listdir())
    HTMLoutput=Markup('<p>Structured HTML</p>')
    
    toscrn = HTMLoutput
    print("**************************CommListFileHandler() flag 17******************************************************")
    

    
    return toscrn





    


    

    




    


    

    

