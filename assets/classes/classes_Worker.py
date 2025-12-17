"""
Program name : class_Worker.py
Authors : Loïc & Samuel
Date : 03.12.2025
Edit : 17.12.2025
Description : class Worker
Version : V 1.0
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from assets.classes.classes_People import Person

class Worker(Person):
    __tablename__ = "workers"

    id = Column(Integer, ForeignKey("people.id"), primary_key=True)
    schedule = Column(String, nullable=False)
    e_mail = Column(String, nullable=False)

    def __init__(self, **kwargs):
        """
        Initialize a Worker instance
        Inherits firstname and lastname from Person
        Sets schedule and e_mail attributes
        """
        super().__init__(**kwargs)
        self.schedule = kwargs.get("Schedule")
        self.e_mail = kwargs.get("e_mail")

    def __repr__(self):
        """
        Return a readable string showing all Worker details
        """
        return (f"id: {self.id}, firstname: {self.firstname}, lastname: {self.lastname}, "
                f"schedule: {self.schedule}, e_mail: {self.e_mail}")



