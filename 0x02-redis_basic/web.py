#!/usr/bin/env python3
"""
Module to implement a web cache and tracker using Redis
"""
import redis
import requests

redis_client = redis.Redis()
request_count = 0


def get_page_and_cache(url: str) -> str:
    """ Get a page and cache value """
    redis_client.set(f"cached:{url}", request_count)
    response = requests.get(url)
    redis_client.incr(f"count:{url}")
    redis_client.setex(f"cached:{url}", 10, redis_client.get(f"cached:{url}"))
    return response.text


if __name__ == "__main__":
    get_page_and_cache('http://slowwly.robertomurray.co.uk')
