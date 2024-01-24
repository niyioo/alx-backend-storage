#!/usr/bin/env python3
"""
Cache module
"""
import redis
import uuid
from typing import Callable, Union
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts how many times a method is called
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to count calls
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    """
    Cache class
    """

    def __init__(self) -> None:
        """
        Initialize Cache instance
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis and return the key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieve data from Redis using key and apply optional conversion function fn
        """
        result = self._redis.get(key)
        if result is not None and fn is not None:
            return fn(result)
        return result

    def get_str(self, key: str) -> Union[str, None]:
        """
        Retrieve string data from Redis using key
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """
        Retrieve integer data from Redis using key
        """
        return self.get(key, fn=int)
