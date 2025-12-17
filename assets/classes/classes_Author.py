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

    id = Column(Integer, ForeignKey("people.id"), primary_key=True)

    def __repr__(self):
        return f"id: {self.id}, firstname: {self.firstname}, lastname: {self.lastname}"


