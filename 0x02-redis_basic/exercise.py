#!/usr/bin/env python3
"""
Cache module
"""
import redis
from uuid import uuid4
from typing import Callable, Optional, Union
from functools import wraps


def record_user_actions(method: Callable) -> Callable:
    """Decorator to log user actions"""
    method_key = method.__qualname__
    inputs_key = method_key + ':inputs'
    outputs_key = method_key + ':outputs'

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapped function to record user actions"""
        self._redis.rpush(inputs_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(outputs_key, str(result))
        return result

    return wrapper


def count_method_calls(method: Callable) -> Callable:
    """Decorator to count method calls"""
    method_key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapped function to count method calls"""
        self._redis.incr(method_key)
        return method(self, *args, **kwargs)

    return wrapper


def display_call_history(method: Callable):
    """Function to display the call history of a method"""
    method_key = method.__qualname__
    inputs_key = method_key + ":inputs"
    outputs_key = method_key + ":outputs"
    redis_instance = method.__self__._redis
    call_count = redis_instance.get(method_key).decode("utf-8")
    print("{} was called {} times:".format(method_key, call_count))
    input_list = redis_instance.lrange(inputs_key, 0, -1)
    output_list = redis_instance.lrange(outputs_key, 0, -1)
    all_data = list(zip(input_list, output_list))
    for input_data, output_data in all_data:
        input_str, output_str = input_data.decode(
            "utf-8"), output_data.decode("utf-8")
        print("{}(*{}) -> {}".format(method_key, input_str, output_str))


class Cache:
    """Class to store information"""

    def __init__(self):
        """Constructor to initialize the instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @record_user_actions
    @count_method_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store new data and return a new UUID"""
        key = str(uuid4())
        self._redis.mset({key: data})
        return key

    def get(
            self,
            key: str,
            fn: Optional[Callable] = None
            ) -> Union[str, bytes, int, float]:
        """Get the element and return the decoded version"""
        data = self._redis.get(key)
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, data: str) -> str:
        """Return the decoded byte in string"""
        return data.decode('utf-8')

    def get_int(self, data: str) -> int:
        """Return the decoded byte in integer"""
        return int(data)
