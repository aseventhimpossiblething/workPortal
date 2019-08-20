#heroku create myapp --buildpack heroku/python
# an object of WSGI application
from flask import Flask
from flask import render_template
app = Flask(__name__)   # Flask constructor

# A decorator used to tells the application
# which URL is associated function
@app.route('/')
def hello():
    return "Hello Mundo"

@app.route('/0')
def hollo():

    return render_template('initial.html')



if __name__=='__main__':
#if '__name__'=='__main__':
#if __bdx-api-link__=='__main__':
#if '__bdx-api-link__'=='__main__':
#if 'bdx-api-link'=='__main__':
#if bdx-api-link=='__main__':
    app.run()

