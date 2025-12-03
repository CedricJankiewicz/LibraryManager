"""
Program name : class_book.py
Author : Loïc
Date : 03.12.2025
Edit : 03.12.2025
Description : class Book
Version : V 1.0
"""

# we need to order the variables like id name front,back
class Book:
    def __init__(self, id,publishing_date,title,back_cover,genre,is_avaible,front_cover,status, author):
        self.id = id
        self.publishing_date = publishing_date
        self.title = title
        self.back_cover = back_cover
        self.genre = genre
        self.is_avaible = is_avaible
        self.front_cover = front_cover
        self.status = status
        self.author = author


""" Exemple to create a book

le_livre_de_la_jungle = Book("344",
                             "07.01,1977",
                             "Le livre de la jungle",
                             "mowgli a été abondonné...",
                             "roman d'aventure",
                             False,
                             "img :jasdkuhafkjfdkjg kgaffjk",
                             "08/10",
                             "Debora Tempest")

print(le_livre_de_la_jungle.id,le_livre_de_la_jungle.publishing_date, le_livre_de_la_jungle.title, le_livre_de_la_jungle.back_cover,le_livre_de_la_jungle.genre,le_livre_de_la_jungle.is_avaible,le_livre_de_la_jungle.front_cover,le_livre_de_la_jungle.status,le_livre_de_la_jungle.author)

"""