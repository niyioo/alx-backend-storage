#!/usr/bin/env python3
"""
9-insert_school.py
"""
import pymongo


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document in a collection based on kwargs.

    Args:
        mongo_collection: pymongo Collection object.
        **kwargs: Key-value pairs for the document attributes.

    Returns:
        The new _id of the inserted document.
    """
    result = mongo_collection.insert_one(kwargs)
    return str(result.inserted_id)
