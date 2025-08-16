from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    community = Column(String)
    tags = Column(String)
    signup_date = Column(DateTime, default=datetime.utcnow)

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    tags = Column(String)
    creator_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    popularity_score = Column(Float, default=0.0)
    likes_count = Column(Integer, default=0)
    views_count = Column(Integer, default=0)
    shares_count = Column(Integer, default=0)

class Interaction(Base):
    __tablename__ = "interactions"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True) 
    user_id = Column(Integer, ForeignKey("users.id"))
    item_id = Column(Integer, ForeignKey("items.id"))
    type = Column(String)
    timestamp = Column(DateTime(timezone=True), default=func.now()) 