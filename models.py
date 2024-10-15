from sqlalchemy import Boolean, Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True, index=True)
    task = Column(Text, nullable=False)
    completed = Column(Boolean, default=False)


class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True, index=True)
    todo_id = Column(Integer, ForeignKey('todos.id'))
    completed_date = Column(DateTime, default=datetime.utcnow)
    task = Column(Text, nullable=False)
