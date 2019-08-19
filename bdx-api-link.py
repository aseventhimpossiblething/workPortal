#heroku create myapp --buildpack heroku/python
# an object of WSGI application
from flask import Flask
app = Flask(__name__)   # Flask constructor

# A decorator used to tells the application
# which URL is associated function
@app.route('/')
def hello():
    return "Hello Mundo"

if __name__=='__main__':
#if '__name__'=='__main__':
#if __bdx-api-link__=='__main__':
#if '__bdx-api-link__'=='__main__':
#if 'bdx-api-link'=='__main__':
#if bdx-api-link=='__main__':
#app.run()
