#!/usr/bin/env python3
"""
Cache module
"""
import redis
from uuid import uuid4
from typing import Callable, Optional, Union
from functools import wraps


def call_history(method: Callable) -> Callable:
    """Decorator to log user actions"""
    method_key = method.__qualname__
    inputs = method_key + ':inputs'
    outputs = method_key + ':outputs'

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """Wrapped function to record user actions"""
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwds)
        self._redis.rpush(outputs, str(data))
        return data
    return wrapper


def count_calls(method: Callable) -> Callable:
    """Decorator to count method calls"""
    method_key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """Wrapped function to count method calls"""
        self._redis.incr(method_key)
        return method(self, *args, **kwds)
    return wrapper


def replay(method: Callable):
    """Function to display the call history of a method"""
    method_key = method.__qualname__
    inputs = method_key + ":inputs"
    outputs = method_key + ":outputs"
    redis = method.__self__._redis
    count = redis.get(method_key).decode("utf-8")
    print("{} was called {} times:".format(method_key, count))
    ListInput = redis.lrange(inputs, 0, -1)
    ListOutput = redis.lrange(outputs, 0, -1)
    allData = list(zip(ListInput, ListOutput))
    for key, data in allData:
        attr, data = key.decode("utf-8"), data.decode("utf-8")
        print("{}(*{}) -> {}".format(method_key, attr, data))


class Cache:
    """
    Class to store information
    """


    def __init__(self):
        """Constructor to initialize the instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()


    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Store new data and return a new UUID"""
        key = str(uuid4())
        self._redis.mset({key: data})
        return key


    def get(self,
            key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """ Get the element and return the decoded version"""
        data = self._redis.get(key)
        if (fn is not None):
            return fn(data)
        return data

    def get_str(self, data: str) -> str:
        """Return the decoded byte in strin"""
        return data.decode('utf-8')

    def get_int(self, data: str) -> int:
        """Return the decoded byte in integer"""
        return int(data)
