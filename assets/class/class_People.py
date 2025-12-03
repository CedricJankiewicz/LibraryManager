"""
Auteur : Loïc
Date de création : 03.12.2025
Description du fichier : class People ;il sera heriter par la suite
V 1.1

Derniere modif date: 03.12.2025
Dernière modif description : Ajout de l'id

"""

class Person:
    def __init__(self,id ,lastname, firstname):
        self.id = id
        self.lastname = lastname
        self.firstname = firstname


"""
exemple de création d'objets


Jack = Person("id","Jack", "John")


print(Jack.id,Jack.lastname, Jack.firstname)

"""





