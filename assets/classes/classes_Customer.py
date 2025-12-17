"""
Program name : class_Customer.py
Authors : Loïc & Samuel
Date : 03.12.2025
Edit : 17.12.2025
Description : class Customer
Version : V 1.0
"""

from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from assets.classes.classes_People import Person


class Customer(Person):
    __tablename__ = "customers"

    # Colonnes ORM
    id = Column(Integer, ForeignKey("people.id"), primary_key=True)
    adress = Column(String)
    phone_number = Column(String)
    e_mail = Column(String)
    birthdate = Column(Date)
    can_borrow = Column(Boolean)

    # Constructeur simple, compatible CRUD
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.adress = kwargs.get("adress")
        self.phone_number = kwargs.get("phone_number")
        self.e_mail = kwargs.get("e_mail")
        self.birthdate = kwargs.get("birthdate")
        self.can_borrow = kwargs.get("can_borrow")

    def __repr__(self):
        return (f"id: {self.id}, firstname: {self.firstname}, lastname: {self.lastname}, "
                f"adress: {self.adress}', phone_number: {self.phone_number}, "
                f"e_mail: {self.e_mail}', can_borrow: {self.can_borrow}")

