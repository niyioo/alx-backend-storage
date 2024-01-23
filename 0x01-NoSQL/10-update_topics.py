#!/usr/bin/env python3
"""
10-update_topics.py
"""
from pymongo.collection import Collection
from typing import List


def update_topics(mongo_collection: Collection, name: str, topics: List[str]) -> None:
    """
    Changes all topics of a school document based on the name.

    Args:
        mongo_collection: pymongo Collection object.
        name: School name to update.
        topics: List of topics to be set for the school.

    Returns:
        None
    """
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})


if __name__ == "__main__":
    pass  # No code is executed when imported
