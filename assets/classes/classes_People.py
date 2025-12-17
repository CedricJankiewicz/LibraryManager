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

    def __init__(self, **kwargs):
        """
               Initialize a Person instance
               Accepts any keyword arguments and sets firstname and lastname
               This allows creation for CRUD operations
               """
        self.firstname = kwargs.get("firstname")
        self.lastname = kwargs.get("lastname")

    def __repr__(self):
        """
                Return a readable string representation of the Person object,
                showing id, firstname, and lastname
        """
        return (f"id: {self.id}, firstname: {self.firstname}, lastname: {self.lastname}")








