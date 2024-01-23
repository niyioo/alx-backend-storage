#!/usr/bin/env python3
"""
101-students.py
"""
from pymongo import MongoClient


def top_students(mongo_collection):
    """
    Returns all students sorted by average score.
    """
    students = mongo_collection.find()

    for student in students:
        total_score = 0
        for topic in student['topics']:
            total_score += topic['score']
        student['averageScore'] = total_score / len(student['topics'])

    return sorted(students, key=lambda x: x['averageScore'], reverse=True)
