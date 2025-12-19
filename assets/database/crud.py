"""
Program name : crud.py
Author: Samuel
Date: 03.12.2025
Edit : 17.12.2025

Description:
This file initializes the CRUD functions.
They allow you to manage any model.
SQLAlchemy

Version : V 1.0

Using ChatGPT for logic and code corrections
"""

# --------------------------- IMPORTS ---------------------------
from database import get_session

# --------------------------- CREATE ---------------------------
def create(model, **data):
    """
    Creates an instance of a model and adds it to the database
    data: dictionary of fields and values
    """
    session = get_session()
    obj = model(**data)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    session.close()
    return obj

# --------------------------- READ ---------------------------
def get(model, object_id):
    """
    Retrieves an object by ID
    """
    session = get_session()
    obj = session.get(model, object_id)
    session.close()
    return obj

def get_by_name(model, name):
    """
    Collect all objects with a certain name
    """
    session = get_session()
    result = session.query(model).filter(model.name == name).all()
    session.close()
    return result

# --------------------------- UPDATE ---------------------------
def update(model, object_id, **data):
    """
    Updates an object with the new values passed in data
    """
    session = get_session()
    obj = session.get(model, object_id)

    if obj is None:
        session.close()
        return "Pas trouvé"

    for attr, value in data.items():
        setattr(obj, attr, value)

    session.commit()
    session.refresh(obj)
    session.close()
    return obj

# --------------------------- DELETE ---------------------------
def delete(model, object_id):
    """
    Deletes an object from the database
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
