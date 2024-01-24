#!/usr/bin/env python3
"""
Module to implement a web cache and tracker using Redis
"""
import requests
from functools import wraps
import redis
from typing import Callable


def cache_and_track(expiration_time: int = 10) -> Callable:
    """
    Decorator to cache and track the number
    of times a function is called

    Args:
    - expiration_time (int): Expiration time
    for cache in seconds (default is 10)

    Returns:
    - Callable: Decorated function
    """
    def decorator(fn: Callable) -> Callable:
        """
        Decorator function to cache and track the number of
        times a URL is accessed

        Args:
        - fn (Callable): Original function to be decorated

        Returns:
        - Callable: Decorated function
        """
        @wraps(fn)
        def wrapper(url: str) -> str:
            """
            Wrapper function to cache and track
            the number of times a URL is accessed

            Args:
            - url (str): URL to fetch

            Returns:
            - str: HTML content of the URL
            """
            redis_client = redis.Redis()
            count_key = f"count:{url}"

            # Increment the access count
            access_count = redis_client.incr(count_key)

            # If the URL is in the cache, retrieve and return it
            cached_result_key = f"cache:{url}"
            cached_result = redis_client.get(cached_result_key)
            if cached_result:
                return cached_result.decode('utf-8')

            # Otherwise, fetch the HTML content using requests
            html_content = fn(url)

            # Cache the result with expiration time
            redis_client.setex(cached_result_key,
                               expiration_time, html_content)

            return html_content

        return wrapper
    return decorator


@cache_and_track()
def get_page(url: str) -> str:
    """
    Function to obtain the HTML content of a URL

    Args:
    - url (str): URL to fetch

    Returns:
    - str: HTML content of the URL
    """
    response = requests.get(url)
    return response.text
