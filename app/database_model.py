
from sqlalchemy import Column, Integer, String, Float

# from sqlalchemy.orm import declarative_base
from app.database import Base
from sqlalchemy import Boolean, DateTime
from datetime import datetime

# Base = declarative_base()

class Product(Base):

    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    quantity = Column(Integer)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)  # unique ID
    email = Column(String, unique=True, index=True, nullable=False)  # login email
    hashed_password = Column(String, nullable=False)  # store hashed password, not plain
    is_active = Column(Boolean, default=True)  # user status
    is_admin = Column(Boolean, default=False)  # role (future use)
    created_at = Column(DateTime, default=datetime.utcnow)  # account creation time

