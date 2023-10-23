#!/usr/bin/env python3
"""This module showcases pagination, a principle/feature of REST API design"""
import csv
from math import ceil
from typing import Sequence, List, Dict


class Server:
    """Server class to paginate a database of popular baby names."""
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset"""
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    @staticmethod
    def index_range(page: int, page_size: int) -> Sequence[int]:
        """Converts page info to list indices for the corresponding page"""
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        return (page - 1) * page_size, page * page_size

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Paginates the dataset and returns the requested page"""
        start, stop = self.index_range(page, page_size)
        return self.dataset()[start:stop]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """Paginates the dataset and returns the requested page"""
        data = self.get_page(page, page_size)
        total = len(self.dataset())
        return {
            'page_size': len(data),
            'page': page,
            'data': data,
            'next_page': page + 1 if self.get_page(page + 1,
                                                   page_size) else None,
            'prev_page': page - 1 if page > 1 else None,
            'total_pages': ceil(total / page_size)
        }


if __name__ == '__main__':
    """Tests the code in this module"""
    server = Server()

    print(server.get_hyper(1, 2))
    print("---")
    print(server.get_hyper(2, 2))
    print("---")
    print(server.get_hyper(100, 3))
    print("---")
    print(server.get_hyper(3000, 100))
