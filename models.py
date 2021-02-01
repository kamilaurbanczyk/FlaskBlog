from database import Base
from sqlalchemy import Column, Integer, String, DateTime


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=False)
    username = Column(String(30), unique=True)
    email = Column(String(100))
    register_date = Column(DateTime)
    