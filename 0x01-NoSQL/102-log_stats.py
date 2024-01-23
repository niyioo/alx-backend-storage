#!/usr/bin/env python3
"""
Python script that provides some stats about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient


METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]


def log_stats(mongo_collection, option=None):
    """
    Provide some stats about Nginx logs stored in MongoDB
    """
    stats = {}
    if option:
        val = mongo_collection.count_documents(
            {"method": {"$regex": option}})
        print(f"\tmethod {option}: {val}")
        return

    result = mongo_collection.count_documents(stats)
    print(f"{result} logs")
    print("Methods:")
    for method in METHODS:
        val = mongo_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {val}")

    status_check = mongo_collection.count_documents({"path": "/status"})
    print(f"{status_check} status check")

    # Top 10 IPs
    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    top_ips = mongo_collection.aggregate(pipeline)

    print("IPs:")
    for entry in top_ips:
        print(f"\t{entry['_id']}: {entry['count']}")


if __name__ == "__main__":
    nginx_collection = MongoClient('mongodb://127.0.0.1:27017').logs.nginx
    log_stats(nginx_collection)
