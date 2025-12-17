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
    publishing_date = Column(String)
    title = Column(String)
    back_cover = Column(String)
    genre = Column(String)
    is_avaible = Column(Boolean)
    front_cover = Column(String)
    status = Column(String)

    #   relation (foreign key)
    author_id = Column(Integer, ForeignKey("authors.id"))

    def __init__(
        self,
        id=None,
        publishing_date=None,
        title=None,
        back_cover=None,
        genre=None,
        is_avaible=None,
        front_cover=None,
        status=None,
        author_id=None
    ):
        self.id = id
        self.publishing_date = publishing_date
        self.title = title
        self.back_cover = back_cover
        self.genre = genre
        self.is_avaible = is_avaible
        self.front_cover = front_cover
        self.status = status
        self.author_id = author_id

    def __repr__(self):
        return (f"id: {self.id}, title: {self.title}, publishing_date: {self.publishing_date}, "
                f"genre: {self.genre}, is_avaible: {self.is_avaible}")

