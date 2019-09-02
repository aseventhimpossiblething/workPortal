import BidOpAssist
from flask import Flask, render_template, request
import os
import psycopg2
def fileHandler():
    print("********************************flag 1************************************************")

    print("request.files______:   ",request.files)

    print("********************************flag 2************************************************")

    print("request.files['sheet']______:    ",request.files['sheet'])

    print("********************************flag 3*************************************************")

    print("request.files['sheet'].filename_______:     ",request.files['sheet'].filename)

    #print("request.files['sheet'].save(os.path.join('/app/Sheets',request.files['sheet'].filename))")

    #request.files['sheet'].save(os.path.join('/app/Sheets',request.files['sheet'].filename))

    #os.chdir(r'/app/Sheets')

    print("*********************************flag 4***********************************************")

    print("os.getcwd()_____: ",os.getcwd())

    #print(request.files['sheet'].save(os.path.join('/app/Sheets/sheet',request.files['sheet'].filename)))

    print("********************************flag 5************************************************")

    print("os.listdir()____:",os.listdir())

    print("********************************flag 6************************************************")

    os.chdir('/app/Sheets')

    print("os.chdir(/Sheets)____:")

    print("********************************flag 7************************************************")

    print("os.getcwd()_____: ",os.getcwd())

    print("********************************flag 8************************************************")

    print("os.listdir()____:",os.listdir())

    print("********************************flag 9************************************************")

    print("request.files['sheet'].save(os.path.join('/app/Sheets',request.files['sheet'].filename))")

    request.files['sheet'].save(os.path.join('/app/Sheets',request.files['sheet'].filename))

    print("********************************flag 10************************************************")

    print("os.getcwd()____:",os.getcwd)

    print("********************************flag 11************************************************")

    print("os.listdir()____:",os.listdir())

    print("********************************flag 12************************************************")

    print("os.path.join('/app/Sheets',request.files['sheet'].filename))_____:",os.path.join('/app/Sheets',request.files['sheet'].filename))

    print("********************************flag 13************************************************")

    print("request.files['sheet'].filename_______:     ",request.files['sheet'].filename)

    print("********************************flag 14************************************************")

    print("request.files['sheet']______:    ",request.files['sheet'])

    print("********************************flag 15************************************************")

    print("request.files______:    ",request.files)

    print("**************************flag 16******************************************************")
    
    topage=str(request.method),"Done!"
    print(topage)
    print("**************************flag 17******************************************************")
    return request.method
