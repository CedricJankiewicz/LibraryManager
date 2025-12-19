"""
Program name : database.py
Author: Samuel
Date: 03.12.2025
Edit : 17.12.2025

Description:
    The database is created and configured for:
    - SQLite connection engine
    - database for models
    - session factory to interact with the database
The file also provides a utility function
that makes it easy to obtain a new session

Version : V 1.0
"""

# --------------------------------- IMPORTS ---------------------------------
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# --------------------------------- ENGINE CONFIGURATION ---------------------------------
engine = create_engine("sqlite:///database.db")

# --------------------------------- DECLARATIVE BASE ---------------------------------
Base = declarative_base()

# --------------------------------- SESSION FACTORY ---------------------------------
SessionLocal = sessionmaker(bind=engine)

# --------------------------------- UTILITY FUNCTION ---------------------------------
def get_session():
    """
    Creates and returns a new SQLAlchemy session
    Used for all CRUD operations
    """
    return SessionLocal()
