
import glob
import numpy
import scipy
import pandas
import BidOpAssist
import fileHandler
from flask import Flask, render_template, request
import os
import psycopg2
from sklearn.ensemble import RandomForestRegressor


#DATABASE_URL = os.environ['DATABASE_URL']


app = Flask(__name__)   # Flask constructor




#conn = psycopg2.connect(DATABASE_URL, sslmode='require')
#conn = psycopg2.connect("dbname='dcect276ul8asc' user='ffsezxsqjvacnw' host='ec2-54-83-9-36.compute-1.amazonaws.com' password='657c149f7aac22520e75d72bddb9a16c76e60ac324fb4358f9f579ac1c2619d4'")

#conn.cursor().execute("SELECT * FROM information_schema.tables ")
#conn.cursor().execute("CREATE TABLE newTable (id int,Data text)")

#print("run __: ",conn.cursor().execute("SELECT * FROM dcect276ul8asc"))
#print('run conn.cursor().execute("SELECT * FROM information_schema.tables")___:', conn.cursor().execute("SELECT * FROM information_schema.tables"))
#print(conn.cursor().execute("SELECT * FROM pg_stat_user_tables"))

#print("attempting to create tables")
#conn.cursor().execute("CREATE TABLE DocumentSubmissions("Documents")")
#conn.cursor().execute("CREATE TABLE storage (user_id serial PRIMARY KEY, username VARCHAR (50) UNIQUE NOT NULL, password VARCHAR (50) NOT NULL, email VARCHAR (355) UNIQUE NOT NULL, created_on TIMESTAMP NOT NULL, last_login TIMESTAMP)")

#conn.cursor().close()
#conn.commit()
#print(conn.cursor().execute("SELECT * FROM pg_stat_user_tables"))
#conn.close

#print(conn.cursor().execute("SELECT * FROM pg_stat_user_tables"))




@app.route('/')
def hello():
    return "Hello le monde"

@app.route('/upload', methods=['POST','GET'])
def upload():
    fileHandler.fileHandler()
    return fileHandler.fileHandler()
      
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
def holld():
    return render_template('fileInput.html') 

@app.route('/3')
def holle():
    return render_template('BidOutput.html',MostRecent="Current Bid op static file",PoutPut=BidOpAssist.BidOpAssist())
 

@app.route('/4')
def hollf():
    return render_template('CommunityUpdate.html')
   



if __name__=='__main__':
    app.run()

