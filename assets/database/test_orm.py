"""
Program name : test_orm.py
Author: Samuel
Date: 03.12.2025
Edit : 17.12.2025

Description:
Simple tests of generic CRUD with models from the class folder.
Used to verify the creation, reading, updating, and
deletion of an object.

Version : V 1.0
"""

# --------------------------- IMPORTS ---------------------------
from assets.classes.classes_Author import *
from assets.classes.classes_Book import Book
from assets.classes.classes_Publisher import Publisher
from assets.classes.classes_Worker import Worker
from assets.classes.classes_Customer import Customer
from assets.database.database import *
from assets.database.crud import *


# --------------------------- CREATE TABLE ---------------------------
Base.metadata.create_all(bind=engine)


# --------------------------- AUTHOR ---------------------------
alice = create(Author, firstname="Alice", lastname="Dupont")
print("Author:", alice)


# --------------------------- CUSTOMER ---------------------------
john = create(Customer, firstname="John", lastname="Joe", adress="Rue du lac 12", birthdate="2009-04-01",
              phone_number="0791234567", e_mail="john@example.com", can_borrow=True)
print("Customer:", john)


# --------------------------- WORKER ---------------------------
worker = create(Worker, firstname="Marc", lastname="Leroy", rank="worker", e_mail="marc@example.com")
print("Worker:", worker)


# --------------------------- PUBLISHER ---------------------------
gallimard = create(Publisher, name="Antoine")
print("Publisher:", gallimard)


# --------------------------- BOOK ---------------------------
book1 = create(Book, publishing_date="07.01.1977", title="Le livre de la jungle",
               back_cover="Mowgli a été abandonné...", genre="roman d'aventure",
               is_avaible=True, front_cover="image", status="08/10",
               author_id=alice.id)
print("Book:", book1)

print(get(Book))
print(get_by(Book, "id", 2))
print(update(Book, 2, title="UnlivreTropbien"))
print(delete(Book, 1))