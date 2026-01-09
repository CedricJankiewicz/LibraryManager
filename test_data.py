# --------------------------- IMPORTS ---------------------------
from assets.classes.classes_Author import *
from assets.classes.classes_Book import Book
from assets.classes.classes_Publisher import Publisher
from assets.classes.classes_Worker import Worker
from assets.classes.classes_Customer import Customer
from assets.database.crud import *

# --------------------------- AUTHOR ---------------------------
create(Author, firstname="Suzanne", lastname="Collins")


# --------------------------- WORKER ---------------------------
create(Worker, firstname="Marc", lastname="Leroy", rank="worker", e_mail="marc@example.com", password="Pa$$w0rd")


# --------------------------- PUBLISHER ---------------------------
create(Publisher, name="Dargo suisse")