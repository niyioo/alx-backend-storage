#!/usr/bin/env python3
"""
Cache module
"""
import redis
import uuid
from typing import Callable, Union, List
from functools import wraps


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

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, None]:
        """
        Retrieve data from Redis and optionally convert it using a function

        Args:
        - key (str): Key associated with the stored data
        - fn (Callable): Function to convert the data (default is None)

        Returns:
        - Union[str, bytes, int, None]: Retrieved data, possibly converted
        """
        result = self._redis.get(key)
        if result is not None and fn is not None:
            return fn(result)
        return result

    def get_str(self, key: str) -> Union[str, None]:
        """
        Retrieve data from Redis and convert it to a string

        Args:
        - key (str): Key associated with the stored data

        Returns:
        - Union[str, None]: Retrieved data as a string
        """
        return self.get(key, fn=lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """
        Retrieve data from Redis and convert it to an integer

        Args:
        - key (str): Key associated with the stored data

        Returns:
        - Union[int, None]: Retrieved data as an integer
        """
        return self.get(key, fn=int)

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


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts how many times a method is called

    Args:
    - method (Callable): Original function to be decorated

    Returns:
    - Callable: Decorated function
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to count calls and execute the original method

        Args:
        - self: Cache instance
        - *args: Variable-length argument list
        - **kwargs: Variable-length keyword argument list

        Returns:
        - Output of the wrapped function
        """
        key = "{}:count".format(method.__qualname__)
        count = self._redis.incr(key)
        print("{} was called {} times".format(method.__qualname__, count))

        # Execute the wrapped function to retrieve the output
        return method(self, *args, **kwargs)

    return wrapper


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


# Decorate Cache methods
Cache.store = call_history(Cache.store)
Cache.store = count_calls(Cache.store)


# Test cases
if __name__ == "__main__":
    # Create a Cache instance
    cache = Cache()

    # Test case for task 0
    key_0 = cache.store("Hello, Redis!")

    # Test case for task 1
    assert cache.get_str(key_0) == "Hello, Redis!"

    # Test case for task 2
    key_2 = cache.store(42)

    # Test case for task 3
    cache.replay(cache.store)
