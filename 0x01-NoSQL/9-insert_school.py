#!/usr/bin/env python3
"""
9-insert_school.py
"""
from pymongo.collection import Collection
from typing import Dict


def insert_school(mongo_collection: Collection, **kwargs: Dict) -> str:
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


if __name__ == "__main__":
    pass  # No code is executed when imported
