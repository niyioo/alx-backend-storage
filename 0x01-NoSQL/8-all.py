#!/usr/bin/env python3
"""
8-all.py
"""
from pymongo.collection import Collection
from typing import List


def list_all(mongo_collection: Collection) -> List[dict]:
    """
    Lists all documents in a collection.

    Args:
        mongo_collection: pymongo Collection object.

    Returns:
        List of documents in the collection.
    """
    return list(mongo_collection.find({}))
