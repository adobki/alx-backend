#!/usr/bin/env python3
"""This module showcases cache retaining policies/algorithms"""
from typing import Any, Union
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """Implements a caching system"""
    def __init__(self):
        super().__init__()

    # def put(self, key: Hashable, item: Any) -> None:
    def put(self, key: Union[str, int, bytes], item: Any) -> None:
        """Adds an item to the cache"""
        # if key is not None and item is not None:
        if key and item:
            self.cache_data[key] = item

    def get(self, key: Union[str, int, bytes]) -> Any:
        """Gets an item from the cache"""
        if key:
            return self.cache_data.get(key)
        return None


if __name__ == '__main__':
    """Tests the code in this module"""
    my_cache = BasicCache()
    my_cache.print_cache()
    my_cache.put('A', 'Hello')
    my_cache.put('B', 'World')
    my_cache.put('C', 'Holberton')
    my_cache.print_cache()
    print(my_cache.get('A'))
    print(my_cache.get('B'))
    print(my_cache.get('C'))
    print(my_cache.get('D'))
    my_cache.print_cache()
    my_cache.put('D', 'School')
    my_cache.put('E', 'Battery')
    my_cache.put('A', 'Street')
    my_cache.print_cache()
    print(my_cache.get('A'))
