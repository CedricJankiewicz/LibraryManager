"""
Program name : class_Author.py
Authors : Loïc & Samuel
Date : 03.12.2025
Edit : 17.12.2025
Description : class Author
Version : V 1.0
"""

from sqlalchemy import Column,Integer, ForeignKey
from assets.classes.classes_People import Person


class Author(Person):
    __tablename__ = "authors"

    id = Column(Integer, ForeignKey("people.id"), primary_key=True, nullable=False)

    def __init__(self, ** kwargs):
        """
        Initialize an Author instance
        Inherits firstname and lastname from Person
        Accepts keyword arguments for future extension
        """
        super().__init__(**kwargs)



    def __repr__(self):
        """
        Return a readable string for Author showing id, firstname, and lastname
        """
        return f"id: {self.id}, firstname: {self.firstname}, lastname: {self.lastname}"




