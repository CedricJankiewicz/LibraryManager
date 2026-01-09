"""
Program name : class_Borrow.py
Authors : Cédric
Date : 08.01.2026
Edit : 08.01.2026
Description : class Borrow
Version : V 1.0
"""
from datetime import datetime
from sqlalchemy import Column, Integer, Boolean, Date, ForeignKey
from assets.database.database import Base

class Borrow(Base):
    __tablename__ = "borrow"

    id = Column(Integer, primary_key=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    returned = Column(Boolean, nullable=False, default=True)

    book_id = Column(Integer, ForeignKey("books.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))

    def __init__(self, **kwargs):
        """
               Initialize a Person instance
               Accepts any keyword arguments and sets firstname and lastname
               This allows creation for CRUD operations
               """
        self.id = kwargs.get("id")
        self.start_date = datetime.strptime(kwargs.get("start_date"), '%d.%m.%Y').date()
        self.end_date = datetime.strptime(kwargs.get("end_date"), '%d.%m.%Y').date()
        self.returned = kwargs.get("returned")

        self.book_id = kwargs.get("book_id")
        self.customer_id = kwargs.get("customer_id")

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"id={self.id}, "
            f"book_id={self.book_id}, "
            f"customer_id={self.customer_id}, "
            f"start_date={self.start_date}, "
            f"end_date={self.end_date}, "
            f"returned={self.returned}"
            f")"
        )