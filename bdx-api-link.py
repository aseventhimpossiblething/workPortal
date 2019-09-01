print("Checkpoint 1-before imports")
import BidOpAssist
import os
import psycopg2
from flask import Flask, render_template, request
app = Flask(__name__)   # Flask constructor
print("Checkpoint 2-before Database connection")
conn = psycopg2.connect("dbname='dcect276ul8asc' user='ffsezxsqjvacnw' host='ec2-54-83-9-36.compute-1.amazonaws.com' password='657c149f7aac22520e75d72bddb9a16c76e60ac324fb4358f9f579ac1c2619d4'")
print("Checkpoint 3-after Database connection")
print(os.getcwd())
print("os.getcwd ran")
print("attempted os.getcwd point passed")
print("will run os.listdir()")
print(os.listdir())
print("attempted os.listdir() point passed")
print("test os.chdir(r'/app/Sheets')")
os.chdir(r'/app/Sheets')
print("ran os.chdir()")
print("Check os.cwd()")
print(os.getcwd())
print("passed os.getcwd")
print("running BidOpAssist")
BidOpAssist.BidOpAssist("Variable Passed")
print("BidOpAssist ran")



@app.route('/')
def hello():
    return "Hello le monde"

@app.route('/upload', methods=['GET','POST'])
def upload():
    print(request.method)
    return request.file
   

@app.route('/css')
def hollb():
    return render_template('csstemplate.css')

@app.route('/0')
def hollo():
    return render_template('initial.html')

@app.route('/1')
def holla():
    return render_template('cssPulling.html')

@app.route('/2')
def hollc():
    return render_template('fileInput.html')






if __name__=='__main__':
    app.run()

