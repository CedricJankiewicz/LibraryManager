"""
Program name : class_Author.py
Author : Loïc
Date : 03.12.2025
Edit : 03.12.2025
Description : class Author
Version : V 1.0
"""

from class_People import *

class Author(Person):
    def __init__(self,id, firstname, lastname):
        super().__init__(id,firstname, lastname)

"""
Exemple to create a Author

Roger_federe = Author("4", "Roger","federer)

print(Roger_federe.id, Roger_federe.firstname, Roger_federe.lastname)

"""
