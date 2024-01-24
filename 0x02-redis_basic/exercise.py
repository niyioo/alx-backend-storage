#!/usr/bin/env python3
"""
Cache module
"""
import redis
import uuid
from typing import Callable, Union, List
from functools import wraps


def call_history(method: Callable) -> Callable:
    """
    Decorator that stores the history of inputs and outputs for a function

    Args:
    - method (Callable): Original function to be decorated

    Returns:
    - Callable: Decorated function
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to store the history

        Args:
        - self: Cache instance
        - *args: Variable-length argument list
        - **kwargs: Variable-length keyword argument list

        Returns:
        - Output of the wrapped function
        """
        inputs_key = "{}:inputs".format(method.__qualname__)
        outputs_key = "{}:outputs".format(method.__qualname__)

        # Store the input arguments
        self._redis.rpush(inputs_key, str(args))

        # Execute the wrapped function to retrieve the output
        output = method(self, *args, **kwargs)

        # Store the output
        self._redis.rpush(outputs_key, output)

        return output

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

    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis and return the key

        Args:
        - data (Union[str, bytes, int, float]): Data to be stored

        Returns:
        - str: Key associated with the stored data
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def replay(self, method: Callable) -> None:
        """
        Replay and display the history of calls for a particular function

        Args:
        - method (Callable): Function for which the history is to be displayed
        """
        inputs_key = "{}:inputs".format(method.__qualname__)
        outputs_key = "{}:outputs".format(method.__qualname__)

        # Retrieve inputs and outputs from Redis
        inputs = self._redis.lrange(inputs_key, 0, -1)
        outputs = self._redis.lrange(outputs_key, 0, -1)

        # Display the history
        print("{} was called {} times:".format(
            method.__qualname__, len(inputs)))
        for input_args, output in zip(inputs, outputs):
            # Convert string back to tuple
            input_args = eval(input_args.decode('utf-8'))
            print("{} -> {}".format(method.__qualname__, tuple(input_args), output))
