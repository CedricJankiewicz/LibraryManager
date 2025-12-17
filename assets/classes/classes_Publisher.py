"""
Program name : class_Publisher.py
Authors : Loïc & Samuel
Date : 03.12.2025
Edit : 17.12.2025
Description : class Publisher
Version : V 1.0
"""

from sqlalchemy import Column, Integer, String
from assets.database.database import Base

class Publisher(Base):
    __tablename__ = "publishers"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

    def __repr__(self):
        return (f"id: {self.id}, name: {self.name}")


