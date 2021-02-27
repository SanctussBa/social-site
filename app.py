from flask import Flask, render_template, request, url_for, redirect, session
# pip install Flask, template-render

from flask_sqlalchemy import SQLAlchemy
#pip install flask-sqlalchemy

from flask_bcrypt import Bcrypt
# pip install Bcrypt

from flask_login import current_user, login_required, LoginManager, login_user, UserMixin, logout_user
# pip install flask-login

from flask_ckeditor import CKEditor
# pip install Flask-CKEditor

import base64
import os
from datetime import datetime




app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
ckeditor = CKEditor(app)

login_manager = LoginManager(app)
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
    comments = db.relationship('Comment', back_populates='comment_author')


class Post(db.Model):
    __tablename__='post'
    id = db.Column(db.Integer, primary_key = True)

    post_date = db.Column(db.DateTime, default=datetime.now)
    votes = db.Column(db.Integer, nullable=True)
    title = db.Column(db.String(50))
    text = db.Column(db.String(400))
    post_picture = db.Column(db.LargeBinary, nullable=True)

    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
    author =  db.relationship('Profile', back_populates='posts')
    post_comments = db.relationship('Comment', back_populates='post')


class Comment(db.Model):
    __tablename__='comment'
    id = db.Column(db.Integer, primary_key = True)
    comment_date = db.Column(db.DateTime, default=datetime.now)
    comment = db.Column(db.String(300))
    comment_reply =  db.Column(db.String(200))

    author_id =  db.Column(db.Integer, db.ForeignKey('profile.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    comment_author = db.relationship('Profile', back_populates='comments')
    post = db.relationship('Post', back_populates='post_comments')

    def __init__(self, comment, comment_date, author_id, post_id):
        self.comment = comment
        self.comment_date = comment_date
        self.author_id = author_id
        self.post_id = post_id


# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
# Custom filter in jinja_env
def b64encode(data):
    return base64.b64encode(data).decode()
    app.jinja_env.filters['b64encode'] = b64encode



@login_manager.user_loader
def load_user(profile_id):
    return Profile.query.get(int(profile_id))

@app.route('/')
def home():
    posts = Post.query.order_by(Post.post_date.desc())
    post_comments = Comment.query.order_by(Comment.comment_date.asc())
    # Necessary for custom filter in jinja
    app.jinja_env.filters['b64encode'] = b64encode
    return render_template('home.html', posts=posts, post_comments=post_comments)

# redirected from def add_comment()
@app.route('/home/post<post_id>')
def home_current_post(post_id):
    posts = Post.query.order_by(Post.post_date.desc())
    app.jinja_env.filters['b64encode'] = b64encode
    return render_template('home.html', posts=posts)

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

@app.route('/profile/<username>')
@login_required
def settings(username):
    i = Profile.query.filter_by(username=username).first()

    profile_pic = base64.b64encode(i.profile_picture).decode('utf-8')
    return render_template('settings.html', profile_pic = profile_pic)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/add_post", methods=['GET', 'POST'] )
@login_required
def add_post():
    if request.method == 'POST':

        try:

            title = request.form.get('title')
            text = request.form.get('ckeditor')


            date = datetime.now()
            # date = datetime_obj.strftime("%d/%m/%Y- %H:%M")

            profile_id = current_user.id
            new_post = Post(post_date=date, title=title, text=text, profile_id = profile_id)
            db.session.add(new_post)
            db.session.commit()

            return redirect(url_for('home'))
        except:
            error = "Something went wrong"
            return render_template('add_post.html', error = error)

    return render_template('add_post.html')



@app.route("/home/comment", methods=['GET', 'POST'])
@login_required
def add_comment():
    if request.method == 'POST':
        # comment_form is a name of submit input button
        if 'comment_form' in request.form:
            #
            # try:
            #
            #     comment_text = request.form.get('comment')
            #     comment_author = current_user.username
            #     author_id = current_user.id
            #     post_id = request.form['hidden']
            #     comment_date = datetime.now()
            #
            #     new_comment = Comment(comment_date=comment_date, comment=comment_text, author_id=author_id, post_id=post_id)
            #
            #     db.session.add(new_comment)
            #     db.session.commit()
            #     return redirect(url_for('home_current_post', post_id=post_id))
            # except:
            #     print("Error")
            #     pass
            comment_text = request.form.get('comment')
            comment_author = current_user.username
            author_id = current_user.id
            post_id = request.form['hidden']
            comment_date = datetime.now()

            new_comment = Comment(comment_date=comment_date, comment=comment_text, author_id=author_id, post_id=post_id)

            db.session.add(new_comment)
            db.session.commit()
            return redirect(url_for('home_current_post', post_id=post_id))
        else:
            print(" comment_form is not in request")
            pass
    return redirect(url_for('home'))


@app.route("/image_handler", methods=['GET', 'POST'])
@login_required
def image_handler():
    if request.method == "POST":
        if 'image' in request.form:

            path = os.path.abspath(os.getcwd())
            username = current_user.username
            image = request.files['image']

            filename = "img.jpg"
            full_path = os.path.join(path, "static/pics","")
            image.save(full_path + filename)

            new_binary_data = open(full_path + "img.jpg", 'rb').read()

            change_pic = Profile.query.filter_by(username=current_user.username).first()
            change_pic.profile_picture = new_binary_data
            db.session.commit()

            os.remove(full_path + "img.jpg")
            return redirect(url_for('settings', username=username))
        else:
            print(" image form is not in request")
            pass
    else:
        return redirect(url_for('settings'))

if __name__ == '__main__':
    app.run()
