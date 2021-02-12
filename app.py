
from flask import Flask, render_template, request, url_for, redirect, session
# pip install Flask, template-render

from flask_sqlalchemy import SQLAlchemy
#pip install flask-sqlalchemy

from flask_bcrypt import Bcrypt
# pip install Bcrypt

from flask_login import current_user, login_required, LoginManager, login_user, UserMixin, logout_user
# pip install flask-login


import base64
import os
from datetime import datetime




app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)


login_manager = LoginManager()
login_manager.init_app(app)

# login_manager.login_view = 'users.login'
# login_manager.login_message_category = 'info'
# _______________________________________________________________________

profile_pic = open('static/pics/default.png', 'rb').read()

class Profile(db.Model, UserMixin):
    __tablename__='profile'
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    profile_picture = db.Column(db.LargeBinary, default=profile_pic, nullable=False)
    posts = db.relationship('Post', back_populates='author')



class Post(db.Model):
    __tablename__='post'
    id = db.Column(db.Integer, primary_key = True)

    date = db.Column(db.DateTime)
    # datetime_object = datetime.utcnow()
    # date = datetime_object.strftime("%d-%m-%Y  %H:%M")

    votes = db.Column(db.Integer)
    title = db.Column(db.String(50))
    text = db.Column(db.String(400))
    post_picture = db.Column(db.LargeBinary)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
    author =  db.relationship('Profile', back_populates='posts')
    post_comments = db.relationship('Comment', back_populates='post')


class Comment(db.Model):
    __tablename__='comment'
    id = db.Column(db.Integer, primary_key = True)

    comment = db.Column(db.String(300))
    post_reply =  db.Column(db.String(200))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', back_populates='post_comments')

    def __repr__(self):
        if reply:
            return f"{self.comment}\n   {self.reply}"
        else:
            return f"{self.comment}"


# -----------------------------------------------------------------------
# -----------------------------------------------------------------------


@login_manager.user_loader
def load_user(profile_id):
    return Profile.query.get(int(profile_id))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():

    if request.method == 'POST':

        try:
            # picture = "../static/pics/default.png"
            n = request.form['name']
            e = request.form['email']
            p = request.form['password']

            new_user = Profile(username = n , email= e, password= p)

            db.session.add(new_user)
            db.session.commit()

            message = "You are successfully registered, please log in!"
            return render_template('log_in.html', message=message)

        except:
            error = "Could not Sign you up. Error Occured. Try again."
            return render_template('sign_in.html', error = error)

    else:
        return render_template('sign_in.html')


@app.route('/log_in', methods=['GET', 'POST'])
def log_in():

    if request.method == 'POST':
        e = request.form['email']
        p = request.form['password']


        if Profile.query.filter_by(email= e, password = p).first():
            profile = Profile.query.filter_by(email = e).first()
            login_user(profile, force=True)
            return render_template('profile.html', profile = profile)

        else:
            error = " Email or/and password is not correct."

            return render_template('log_in.html', error = error)



    return render_template('log_in.html')


@app.route('/profile', methods=['GET', 'POST'] )
@login_required
def profile():

    return render_template('profile.html')

@app.route('/settings/<username>')
@login_required
def settings(username):
    profile_pic = base64.b64encode(current_user.profile_picture).decode('utf-8')
    return render_template('settings.html', profile_pic = profile_pic)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
if __name__ == '__main__':
    app.run()
