#!/usr/bin/env python3
"""
11-schools_by_topic.py
"""
from pymongo.collection import Collection
from typing import List


def schools_by_topic(mongo_collection: Collection, topic: str) -> List[dict]:
    """
    Returns the list of schools having a specific topic.

    Args:
        mongo_collection: pymongo Collection object.
        topic: Topic to search.

    Returns:
        List of schools with the specified topic.
    """
    return list(mongo_collection.find({"topics": topic}))


if __name__ == "__main__":
    pass  # No code is executed when imported
