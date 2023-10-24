#!/usr/bin/env python3
"""This module showcases cache retaining policies/algorithms"""
from typing import Any, Union
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """Implements a LIFO/stack caching system"""
    def __init__(self):
        super().__init__()

    def put(self, key: Union[str, int, bytes], item: Any) -> None:
        """Adds an item to the cache using the LIFO algorithm (a stack)"""
        if key and item:
            # Delete key if it exists so it's added to top of stack
            if self.cache_data.get(key):
                del self.cache_data[key]

            # Remove last item in cache if stack is full
            if len(self.cache_data.keys()) >= self.MAX_ITEMS:
                last = list(self.cache_data.keys())[-1]
                del self.cache_data[last]
                print(f'DISCARD: {last}')

            # Add new item to top of stack
            self.cache_data[key] = item

    def get(self, key: Union[str, int, bytes]) -> Any:
        """Gets an item from the cache"""
        if key:
            return self.cache_data.get(key)
        return None


if __name__ == '__main__':
    """Tests the code in this module"""
    my_cache = LIFOCache()
    my_cache.put("A", "Hello")
    my_cache.put("B", "World")
    my_cache.put("C", "Holberton")
    my_cache.put("D", "School")
    my_cache.print_cache()
    my_cache.put("E", "Battery")
    my_cache.print_cache()
    my_cache.put("C", "Street")
    my_cache.print_cache()
    my_cache.put("F", "Mission")
    my_cache.print_cache()
    my_cache.put("G", "San Francisco")
    my_cache.print_cache()
