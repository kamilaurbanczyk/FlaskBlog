from database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=False)
    username = Column(String(30), unique=True)
    email = Column(String(100))
    register_date = Column(DateTime)
    articles = relationship('Article', backref='user', lazy=True)


class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    author = Column(String(30))
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    body = Column(Text)
    date = Column(DateTime)