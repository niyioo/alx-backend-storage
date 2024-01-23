#!/usr/bin/env python3
"""
Python function that returns the list of school having a specific topic
"""
import pymongo


def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of schools having a specific topic.

    Args:
        mongo_collection: pymongo Collection object.
        topic: Topic to search.

    Returns:
        List of schools with the specified topic.
    """
    return list(mongo_collection.find({"topics": topic}))

