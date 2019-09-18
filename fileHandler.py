import BidOpAssist
from flask import Flask, render_template, request
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

    #print("request.files['sheet'].save(os.path.join('/app/Sheets',request.files['sheet'].filename))")

    #request.files['sheet'].save(os.path.join('/app/Sheets',request.files['sheet'].filename))

    #os.chdir(r'/app/Sheets')

    print("*********************************BidOpFileHandler() flag 4***********************************************")

    print("os.getcwd()_____: ",os.getcwd())

    #print(request.files['sheet'].save(os.path.join('/app/Sheets/sheet',request.files['sheet'].filename)))

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

    #print("request.files['sheet'].save(os.path.join('/app/Sheets',request.files['sheet'].filename))")

    #request.files['sheet'].save(os.path.join('/app/Sheets',request.files['sheet'].filename))
    #request.files['sheet'].save(os.path.join('/app/Sheets',request.files['sheet'].filename))


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
    print("********************************CommListFileHandler() flag 1************************************************")

    print("request.files______:   ",request.files)

    print("********************************CommListFileHandler() flag 2************************************************")

    print("request.files['sheet']______:    ",request.files['sheet'])

    print("********************************CommListFileHandler()) flag 3*************************************************")

    print("request.files['sheet'].filename_______:     ",request.files['sheet'].filename)

    #print("request.files['sheet'].save(os.path.join('/app/Sheets',request.files['sheet'].filename))")

    #request.files['sheet'].save(os.path.join('/app/Sheets',request.files['sheet'].filename))

    #os.chdir(r'/app/Sheets')

    print("*********************************CommListFileHandler() flag 4***********************************************")

    print("os.getcwd()_____: ",os.getcwd())

    #print(request.files['sheet'].save(os.path.join('/app/Sheets/sheet',request.files['sheet'].filename)))

    print("********************************CommListFileHandler() flag 5************************************************")

    print("os.listdir()____:",os.listdir())

    print("********************************CommListFileHandler() flag 6************************************************")

    os.chdir('/app/Sheets')

    print("os.chdir(/Sheets)____:")

    print("********************************CommListFileHandler() flag 7************************************************")

    print("os.getcwd()_____: ",os.getcwd())

    print("********************************CommListFileHandler() flag 8************************************************")

    print("os.listdir()____:",os.listdir())

    print("********************************CommListFileHandler() flag 9************************************************")

    #print("request.files['sheet'].save(os.path.join('/app/Sheets',request.files['sheet'].filename))")

    #request.files['sheet'].save(os.path.join('/app/Sheets',request.files['sheet'].filename))
    #request.files['sheet'].save(os.path.join('/app/Sheets',request.files['sheet'].filename))


    request.files['sheet'].save(request.files['sheet'].filename)

    print("********************************CommListFileHandler() flag 10************************************************")

    print("os.getcwd()____:",os.getcwd)

    print("********************************CommListFileHandler() flag 11************************************************")

    print("os.listdir()____:",os.listdir())

    print("********************************CommListFileHandler() flag 12************************************************")

    print("os.path.join('/app/Sheets',request.files['sheet'].filename))_____:",os.path.join('/app/Sheets',request.files['sheet'].filename))

    print("********************************CommListFileHandler() flag 13************************************************")

    print("request.files['sheet'].filename_______:     ",request.files['sheet'].filename)

    print("********************************CommListFileHandler() flag 14************************************************")

    print("request.files['sheet']______:    ",request.files['sheet'])

    print("********************************CommListFileHandler() flag 15************************************************")

    print("request.files______:    ",request.files)

    print("**************************CommListFileHandler() flag 16******************************************************")
    
    toscrn = "done"
    print("**************************CommListFileHandler() flag 17******************************************************")

    
    return toscrn



def CurrentGoogleFileHandler():
    print("********************************CurrentGoogleFileHandler() flag 1************************************************")

    print("request.files______:   ",request.files)

    print("********************************CurrentGoogleFileHandler() flag 2************************************************")

    print("request.files['sheet']______:    ",request.files['sheet'])

    print("********************************CurrentGoogleFileHandler() flag 3*************************************************")

    print("request.files['sheet'].filename_______:     ",request.files['sheet'].filename)

    #print("request.files['sheet'].save(os.path.join('/app/Sheets',request.files['sheet'].filename))")

    #request.files['sheet'].save(os.path.join('/app/Sheets',request.files['sheet'].filename))

    #os.chdir(r'/app/Sheets')

    print("*********************************CurrentGoogleFileHandler() flag 4***********************************************")

    print("os.getcwd()_____: ",os.getcwd())

    #print(request.files['sheet'].save(os.path.join('/app/Sheets/sheet',request.files['sheet'].filename)))

    print("********************************CurrentGoogleFileHandler() flag 5************************************************")

    print("os.listdir()____:",os.listdir())

    print("********************************CurrentGoogleFileHandler() flag 6************************************************")

    os.chdir('/app/Sheets')

    print("os.chdir(/Sheets)____:")

    print("********************************CurrentGoogleFileHandler() flag 7************************************************")

    print("os.getcwd()_____: ",os.getcwd())

    print("********************************CurrentGoogleFileHandler() flag 8************************************************")

    print("os.listdir()____:",os.listdir())

    print("********************************CurrentGoogleFileHandler() flag 9************************************************")

    #print("request.files['sheet'].save(os.path.join('/app/Sheets',request.files['sheet'].filename))")

    #request.files['sheet'].save(os.path.join('/app/Sheets',request.files['sheet'].filename))
    #request.files['sheet'].save(os.path.join('/app/Sheets',request.files['sheet'].filename))


    request.files['sheet'].save(request.files['sheet'].filename)

    print("********************************CurrentGoogleFileHandler() flag 10************************************************")

    print("os.getcwd()____:",os.getcwd)

    print("********************************CurrentGoogleFileHandler() flag 11************************************************")

    print("os.listdir()____:",os.listdir())

    print("********************************CurrentGoogleFileHandler() flag 12************************************************")

    print("os.path.join('/app/Sheets',request.files['sheet'].filename))_____:",os.path.join('/app/Sheets',request.files['sheet'].filename))

    print("********************************CurrentGoogleFileHandler() flag 13************************************************")

    print("request.files['sheet'].filename_______:     ",request.files['sheet'].filename)

    print("********************************CurrentGoogleFileHandler()) flag 14************************************************")

    print("request.files['sheet']______:    ",request.files['sheet'])

    print("********************************CurrentGoogleFileHandler() flag 15************************************************")

    print("request.files______:    ",request.files)

    print("**************************CurrentGoogleFileHandler() flag 16******************************************************")
    
    toscrn = "done"
    print("**************************CurrentGoogleFileHandler() flag 17******************************************************")

    
    return toscrn



def CurrentBingFileHandler():
    print("********************************CurrentBingFileHandler() flag 1************************************************")

    print("request.files______:   ",request.files)

    print("********************************CurrentBingFileHandler() flag 2************************************************")

    print("request.files['sheet']______:    ",request.files['sheet'])

    print("********************************CurrentBingFileHandler() flag 3*************************************************")

    print("request.files['sheet'].filename_______:     ",request.files['sheet'].filename)

    #print("request.files['sheet'].save(os.path.join('/app/Sheets',request.files['sheet'].filename))")

    #request.files['sheet'].save(os.path.join('/app/Sheets',request.files['sheet'].filename))

    #os.chdir(r'/app/Sheets')

    print("*********************************CurrentBingFileHandler() flag 4***********************************************")

    print("os.getcwd()_____: ",os.getcwd())

    #print(request.files['sheet'].save(os.path.join('/app/Sheets/sheet',request.files['sheet'].filename)))

    print("********************************CurrentBingFileHandler() flag 5************************************************")

    print("os.listdir()____:",os.listdir())

    print("********************************CurrentBingFileHandler() flag 6************************************************")

    os.chdir('/app/Sheets')

    print("os.chdir(/Sheets)____:")

    print("********************************CurrentBingFileHandler() flag 7************************************************")

    print("os.getcwd()_____: ",os.getcwd())

    print("********************************CurrentBingFileHandler() flag 8************************************************")

    print("os.listdir()____:",os.listdir())

    print("********************************CurrentBingFileHandler() flag 9************************************************")

    #print("request.files['sheet'].save(os.path.join('/app/Sheets',request.files['sheet'].filename))")

    #request.files['sheet'].save(os.path.join('/app/Sheets',request.files['sheet'].filename))
    #request.files['sheet'].save(os.path.join('/app/Sheets',request.files['sheet'].filename))


    request.files['sheet'].save(request.files['sheet'].filename)

    print("********************************CurrentBingFileHandler() flag 10************************************************")

    print("os.getcwd()____:",os.getcwd)

    print("********************************CurrentBingFileHandler() flag 11************************************************")

    print("os.listdir()____:",os.listdir())

    print("********************************CurrentBingFileHandler() flag 12************************************************")

    print("os.path.join('/app/Sheets',request.files['sheet'].filename))_____:",os.path.join('/app/Sheets',request.files['sheet'].filename))

    print("********************************CurrentBingFileHandler() flag 13************************************************")

    print("request.files['sheet'].filename_______:     ",request.files['sheet'].filename)

    print("********************************CurrentBingFileHandler() flag 14************************************************")

    print("request.files['sheet']______:    ",request.files['sheet'])

    print("********************************CurrentBingFileHandler() flag 15************************************************")

    print("request.files______:    ",request.files)

    print("**************************CurrentBingFileHandler() flag 16******************************************************")
    
    toscrn = "done"
    print("**************************CurrentBingFileHandler() flag 17******************************************************")
    

    
    return toscrn


    


    

    




    


    

    

