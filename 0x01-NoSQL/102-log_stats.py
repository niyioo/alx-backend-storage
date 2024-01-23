#!/usr/bin/env python3
"""
102-log_stats.py
"""
from pymongo import MongoClient


def log_stats(mongo_collection):
    """
    Provides stats about Nginx logs stored in MongoDB.
    """
    total_logs = mongo_collection.count_documents({})
    print(f"{total_logs} logs")

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = mongo_collection.count_documents({"method": method})
        print(f"method {method}: {count}")

    status_check_count = mongo_collection.count_documents({"method": "GET", "path": "/status"})
    print(f"status check: {status_check_count}")

    # Top 10 IPs
    top_ips = mongo_collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])

    print("IPs:")
    for ip_data in top_ips:
        ip = ip_data["_id"]
        count = ip_data["count"]
        print(f"    {ip}: {count}")


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx

    log_stats(logs_collection)
