"""
Program name : crud.py
Author: Samuel
Date: 03.12.2025
Edit : 19.12.2025

Description:
This file initializes the CRUD functions.
They allow you to manage any model.
SQLAlchemy

Version : V 1.0

Using ChatGPT for logic and code corrections
"""

# --------------------------- IMPORTS ---------------------------
from assets.database.database import get_session
# --------------------------- CREATE ---------------------------


def create(model, **data):
    """
    create a new object in the db
    :param model: the table to create in
    :param data: the data of the new object
    :return: the object created
    """
    session = get_session()
    obj = model(**data)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    session.close()
    return obj


# --------------------------- READ ---------------------------


def get(model):
    """
    get every object in a table
    :param model: the table to get
    :return: the results objects
    """
    session = get_session()
    obj = session.query(model).all()  # <-- fetches all rows
    session.close()
    return obj


def get_by(model, by, search):
    """
    search with a like on a table
    :param model: the table to get
    :param by: the column to look at
    :param search: the search data
    :return: the search results
    """
    session = get_session()
    column = getattr(model, by)
    result = session.query(model).filter(column.ilike(f"%{search}%")).all()
    session.close()
    return result


# --------------------------- UPDATE ---------------------------


def update(model, object_id, **data):
    """
    update a object in the db
    :param model: the table to use
    :param object_id: the object to edit
    :param data: the data to change
    :return: the edited object
    """
    session = get_session()
    obj = session.get(model, object_id)

    if obj is None:
        session.close()
        return False

    for attr, value in data.items():
        setattr(obj, attr, value)

    session.commit()
    session.refresh(obj)
    session.close()
    return obj


# --------------------------- DELETE ---------------------------


def delete(model, object_id):
    """
    delete an object in the db
    :param model: the table to use
    :param object_id: the object to delete
    :return: if deleted or not
    """
    session = get_session()
    obj = session.get(model, object_id)

    if obj is None:
        session.close()
        return False

    session.delete(obj)
    session.commit()
    session.close()
    return True