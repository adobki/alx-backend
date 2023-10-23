#!/usr/bin/env python3
"""This module showcases pagination, a principle/feature of REST API design"""
from typing import Sequence


def index_range(page: int, page_size: int) -> Sequence[int]:
    """Converts page info to list indices for the corresponding page"""
    if not isinstance(page, int) or not isinstance(page_size, int):
        raise TypeError('page and page_size must be integers')
    if page <= 0 or page_size <= 0:
        raise ValueError('page and page_size must be >= 1')

    return (page - 1) * page_size, page * page_size


if __name__ == '__main__':
    """Tests the code in this module"""
    res = index_range(1, 7)
    print(type(res))
    print(res)

    res = index_range(page=3, page_size=15)
    print(type(res))
    print(res)
