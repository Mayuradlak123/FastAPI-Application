from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Quiz(Base):
    __tablename__ = "quiz"
    
    id = Column(Integer, primary_key=True, index=True)
    admin_username = Column(String, index=True)
    question = Column(String, index=True)
    answer = Column(String, index=True)
    marks = Column(Integer, default=10)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    score = Column(Integer, default=0)
    submit_count = Column(Integer, default=0)
