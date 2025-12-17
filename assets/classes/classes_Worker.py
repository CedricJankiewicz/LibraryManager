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
    Schedule = Column(String)
    e_mail = Column(String)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.Schedule = kwargs.get("Schedule")
        self.e_mail = kwargs.get("e_mail")

    def __repr__(self):
        return (f"id: {self.id}, firstname: {self.firstname}, lastname: {self.lastname}, "
                f"Schedule: {self.Schedule}, e_mail: {self.e_mail}")



