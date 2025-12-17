"""
Program name : class_People.py
Authors : Loïc & Samuel
Date : 03.12.2025
Edit : 17.12.2025
Description : class People
Version : V 1.0
"""
from sqlalchemy import Column, Integer, String
from assets.database.database import Base

class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)

    def __repr__(self):
        return (f"id: {self.id}, firstname: {self.firstname}, lastname: {self.lastname}")








