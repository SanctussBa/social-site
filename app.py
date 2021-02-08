from flask import Flask, render_template, request, url_for, redirect
# pip install Flask, template-render

from flask_sqlalchemy import SQLAlchemy
#pip install flask-sqlalchemy

from flask_bcrypt import Bcrypt
# pip install Bcrypt




import os
from datetime import datetime

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():

    if request.method == 'POST':
        from models import Profile, Post, Comment

        n = request.form['name']
        e = request.form['email']
        p = request.form['password']

        print(n)
        print(e)
        print(p)

        new_user = Profile(username = n , email= e, password= p)

        db.session.add(new_user)
        db.session.commit()

        message = "You are successfully registered, please log in!"
        return render_template('log_in.html', message=message)
        # try:
        #     # picture = "../static/pics/default.png"
        #     n = request.form['name']
        #     e = request.form['email']
        #     p = request.form['password']
        #
        #     print(n)
        #     print(e)
        #     print(p)
        #
        #     new_user = Profile(username = n , email= e, password= p)
        #
        #     db.session.add(new_user)
        #     db.session.commit()
        #
        #     message = "You are successfully registered, please log in!"
        #     return render_template('log_in.html', message=message)
        #
        # except:
        #     error = "Could not Sign you up. Error Occured. Try again."
        #     return render_template('sign_in.html', error = error)

    else:
        return render_template('sign_in.html')
@app.route('/log_in', methods=['GET', 'POST'])
def log_in():
    return render_template('log_in.html')



if __name__ == '__main__':
    app.run()
