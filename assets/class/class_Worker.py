"""
Auteur : Loïc
Date de création : 03.12.2025
Description du fichier : class Worker hérite nom prénom de people
V 1.1

Derniere modif date: 03.12.2025
Dernière modif description : Ajout de l'id

"""
from class_People import *


class Worker(Person):
    def __init__(self,id,firstname,lastname,Schedule,e_mail):
        super().__init__(id,firstname,lastname)
        self.Schedule = Schedule
        self.e_mail = e_mail

"""   
Exemple d'objets

Jack = Worker("1",jack","Johnes","09-25-45","jack.johnes@eduvaud.ch")

print(Jack.id,Jack.firstname,Jack.lastname,Jack.Schedule,Jack.e_mail)

"""



