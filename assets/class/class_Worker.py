"""
Program name : class_Worker.py
Author : Loïc
Date : 03.12.2025
Edit : 03.12.2025
Description : class Worker
Version : V 1.0
"""

from class_People import *


class Worker(Person):
    def __init__(self,id,firstname,lastname,Schedule,e_mail):
        super().__init__(id,firstname,lastname)
        self.Schedule = Schedule
        self.e_mail = e_mail

"""   
Exemple to create a Worker

Jack = Worker("1",jack","Johnes","09-25-45","jack.johnes@eduvaud.ch")

print(Jack.id,Jack.firstname,Jack.lastname,Jack.Schedule,Jack.e_mail)

"""



