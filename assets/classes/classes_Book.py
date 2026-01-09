"""
Program name : class_book.py
Authors : Loïc & Samuel
Date : 03.12.2025
Edit : 17.12.2025
Description : class Book
Version : V 1.0
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from assets.database.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    publishing_date = Column(String, nullable=False)
    title = Column(String, nullable=False)
    back_cover = Column(String)
    genre = Column(String)
    is_avaible = Column(Boolean, nullable=False, default=True)
    front_cover = Column(String)
    status = Column(String)

    author_id = Column(Integer, nullable=False)
    publisher_id = Column(Integer, nullable=False)

    #   relation (foreign key)
    #author_id = Column(Integer, ForeignKey("authors.id"))
    #publisher_id = Column(Integer, ForeignKey("publishers.id"))

    def __init__(self, **kwargs):
        """
        Initialize a Book instance
        Accepts keyword arguments for all attributes
        Sets default is_avaible to True if not provided
        """
        self.publishing_date = kwargs.get("publishing_date")
        self.title = kwargs.get("title")
        self.back_cover = kwargs.get("back_cover")
        self.genre = kwargs.get("genre")
        self.is_avaible = kwargs.get("is_avaible", True)
        self.front_cover = kwargs.get("front_cover")
        self.status = kwargs.get("status")
        self.author_id = kwargs.get("author_id")
        self.publisher_id = kwargs.get("publisher_id")

    def __repr__(self):
        """
        Return a readable string showing key Book details
        """
        return (f"id: {self.id}, title: {self.title}, publishing_date: {self.publishing_date}, "
                f"genre: {self.genre}, is_avaible: {self.is_avaible}")

