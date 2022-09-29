from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy import TIMESTAMP, Column, Integer, String
from .database import Base

class Task(Base):
    __tablename__ = "tasks"

    Task_ID = Column(Integer, primary_key=True, nullable=False)
    Task = Column(String(255), nullable=False)
    Status = Column(String(45), nullable=False)
    Created_at = Column(TIMESTAMP(timezone=True), server_default = text('now()'),nullable=False)

class User(Base):
    __tablename__ = "users"

    User_ID = Column(Integer, primary_key = True, nullable=False)
    Email = Column(String(255), unique = True, nullable = False)
    Password = Column(String(255), nullable = False)
    Created_at = Column(TIMESTAMP(timezone=True), server_default = text('now()'), nullable = False)
