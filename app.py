from flask import Flask, render_template, request, url_for, redirect
# pip install Flask, template-render

from flask_sqlalchemy import SQLAlchemy
#pip install flask-sqlalchemy

from flask_bcrypt import Bcrypt
# pip install Bcrypt



import os


app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)



@app.route('/sign_in')
def sign_in():
    return render_template('sign_in.html')


@app.route('/log_in')
def log_in():
    return render_template('log_in.html')


@app.route('/')
def home():
    return render_template('home.html')
if __name__ == '__main__':
    app.run()
