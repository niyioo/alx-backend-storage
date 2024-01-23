#!/usr/bin/env python3
"""
Python script that provides some stats about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient


HTTP_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]


def analyze_logs(log_collection, specific_method=None):
    """
    Provide statistics about Nginx logs stored in MongoDB.
    """
    stats = {}

    if specific_method:
        method_count = log_collection.count_documents({"method": {"$regex": specific_method}})
        print(f"\tMethod {specific_method}: {method_count}")
        return

    total_logs = log_collection.count_documents({})
    print(f"{total_logs} logs")
    print("Methods:")

    for method in HTTP_METHODS:
        analyze_logs(log_collection, method)

    status_check_count = log_collection.count_documents({"path": "/status"})
    print(f"{status_check_count} status check")

if __name__ == "__main__":
    nginx_logs = MongoClient('mongodb://127.0.0.1:27017').logs.nginx
    analyze_logs(nginx_logs)

