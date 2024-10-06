# app/db/__init__.py

from .mongodb import MongoDBConnection  # Ensure you import the correct class from the correct file

__all__ = ["MongoDBConnection"]  # Expose the MongoDBConnection class
