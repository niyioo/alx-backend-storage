#!/usr/bin/env python3
"""
8-all.py
"""
import pymongo


def list_all(mongo_collection)
    """
    Lists all documents in a collection.

    Args:
        mongo_collection: pymongo Collection object.

    Returns:
        List of documents in the collection.
    """
    return list(mongo_collection.find()) if mongo_collection else []
