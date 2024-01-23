#!/usr/bin/env python3
"""
Python script that provides some stats about Nginx logs stored in MongoDB
"""
from pymongo.collection import Collection
from pymongo import MongoClient


METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]


def count_documents_with_option(collection: Collection, option: str) -> int:
    """
    Count documents in the collection with a specific option.
    """
    return collection.count_documents({"method": {"$regex": option}})


def log_stats(collection: Collection, option: str = None) -> None:
    """
    Provide some stats about Nginx logs stored in MongoDB.
    """
    if option:
        value = count_documents_with_option(collection, option)
        print(f"\tmethod {option}: {value}")
    else:
        total_logs = collection.count_documents({})
        print(f"{total_logs} logs")
        print("Methods:")
        for method in METHODS:
            log_stats(collection, method)
        status_check = count_documents_with_option(collection, "/status")
        print(f"{status_check} status check")


if __name__ == "__main__":
    mongo_client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = mongo_client.logs.nginx
    log_stats(nginx_collection)
