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
    name = Column(String, nullable=False)

    def __init__(self, **kwargs):
        """
        Initialize a Publisher instance
        Sets the name attribute. ID is handled by the database automatically
        """
        self.name = kwargs.get("name")

    def __repr__(self):
        """
        Return a readable string showing Publisher id and name
        """
        return (f"id: {self.id}, name: {self.name}")


