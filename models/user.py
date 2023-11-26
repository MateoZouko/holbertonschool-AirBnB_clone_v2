#!/usr/bin/python3
"""This module defines a class User"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from models.base_model import BaseModel, Base
from os import getenv

class User(BaseModel, Base):
    """A class to represent a user."""
    __tablename__ = 'users'

    if getenv("HBNB_TYPE_STORAGE") == "db":
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""