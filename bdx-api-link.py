print("Checkpoint 1-before imports")
import os
import psycopg2
from flask import Flask
from flask import render_template
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
print("test os.chdir("app/Sheets")")
os.chdir("/app/Sheets")
print("failed os.chdir() move on ")



@app.route('/')
def hello():
    return "Hello le monde"

@app.route('/0')
def hollo():
    return render_template('initial.html')

@app.route('/1')
def holla():
    return render_template('cssPulling.html')

@app.route('/2', methods=['GET'])
def hollb():
    return render_template('csstemplate.css')






if __name__=='__main__':
    app.run()

