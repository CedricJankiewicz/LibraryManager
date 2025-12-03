"""
Auteur : Loïc
Date de création : 03.12.2025
Description du fichier : classCustomer
V 1.0

Derniere modif date: 03.12.2025
Dernière modif description :

"""
from class_People import *


class Customer(Person):
    def __init__(self, id, firstname, lastname,adress,phone_number, e_mail,birthdate,can_borrow):
        super().__init__(id,firstname, lastname)
        self.adress = adress
        self.phone_number = phone_number
        self.e_mail = e_mail
        self.birthdate = birthdate
        self.can_borrow = can_borrow


"""
Exemple d'objets

Jean = Customer(3654,"Jean","Dumas","chemin j'ai faim","079 875 81 98","Jean.dumas@eduvaud.ch","04.03.2001",True)
"""