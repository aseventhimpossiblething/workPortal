print("Checkpoint 1-before imports")
import BidOpAssist
import os
import psycopg2
from flask import Flask, render_template, request
app = Flask(__name__)   # Flask constructor
print("Checkpoint 2-before Database connection")
conn = psycopg2.connect("dbname='dcect276ul8asc' user='ffsezxsqjvacnw' host='ec2-54-83-9-36.compute-1.amazonaws.com' password='657c149f7aac22520e75d72bddb9a16c76e60ac324fb4358f9f579ac1c2619d4'")




@app.route('/')
def hello():
    return "Hello le monde"

@app.route('/upload', methods=['POST','GET'])
def upload():
    print(request.files)
    request.files['sheet'].save(os.path.join('/app/Sheets',request.files['sheet'].filename))
    #os.chdir(r'/app/Sheets')
    print(request.form)
    print("**************************flag******************************")
    #print(request.files['sheet'].save(os.path.join('/app/Sheets/sheet',request.files['sheet'].filename)))
    print(os.getcwd())
    print(os.path.join('//app/Sheets'/,request.files['sheet']/.filename))
    print(request.files['sheet'].filename)
    print(request.files['sheet'])
    print(request.files)
    print("**************************flag******************************")
    return request.method
   

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

