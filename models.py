from app import db
from sqlalchemy import Integer, String, DateTime, ForeignKey, Text


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(50), unique=False)
    username = db.Column(String(30), unique=True)
    email = db.Column(String(100))
    register_date = db.Column(DateTime)
    articles = db.relationship('Article', backref='user', lazy=True)


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(Integer, primary_key=True)
    title = db.Column(String(100))
    author = db.Column(String(30))
    user_id = db.Column(Integer, ForeignKey('users.id'), nullable=False)
    body = db.Column(Text)
    date = db.Column(DateTime)