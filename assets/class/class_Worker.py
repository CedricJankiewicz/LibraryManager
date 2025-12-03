"""
Auteur : Loïc
Date de création : 03.12.2025
Description du fichier : class Worker herite nom prenom de people
V 1.0

Derniere modif date: 03.12.2025
Dernière modif description :

"""
from class_People import *


class Worker(Person):
    def __init__(self,firstname,lastname,Schedule,e_mail):
        super().__init__(firstname,lastname)
        self.Schedule = Schedule
        self.e_mail = e_mail

"""
Exemple d'objets

Jack = Worker("jack","Johnes","09-25-45","jack.johnes@eduvaud.ch")

print(Jack.firstname,Jack.lastname,Jack.Schedule,Jack.e_mail)

"""



