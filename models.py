from app import db
from datetime import datetime

class Profile(db.Model):
    __tablename__='profile'
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    profile_picture = db.Column(db.LargeBinary)
    posts = db.relationship('Post', back_populates='profile')


class Post(db.Model):
    __tablename__='post'
    id = db.Column(db.Integer, primary_key = True)

    date = db.Column(db.DateTime, default=datetime.utcnow)
    votes = db.Column(db.Integer)
    title = db.Column(db.String(50))
    text = db.Column(db.String(400))
    post_picture = db.Column(db.LargeBinary)
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
