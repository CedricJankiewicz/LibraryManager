"""
Auteur : Loïc
Date de création : 03.12.2025
Description du fichier : class Auhtor
V 1.0

Derniere modif date: 03.12.2025
Dernière modif description :

"""
from class_People import *

class Author(Person):
    def __init__(self,id, firstname, lastname):
        super().__init__(id,firstname, lastname)

"""
Exemple d'objets

Roger_federe = Author("4", "Roger","federer)

print(Roger_federe.id, Roger_federe.firstname, Roger_federe.lastname)



"""
