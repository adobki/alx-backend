#!/usr/bin/env python3
"""This module showcases deletion-resilient hypermedia pagination of HATEOAS"""
import csv
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names."""
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset"""
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]
        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0"""
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            # truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """Paginates the dataset and accounts for deletions on page switch"""
        if index is not None:
            assert isinstance(index, int) and len(self.dataset()) > index >= 1
        else:
            index = 0
        assert isinstance(page_size, int) and page_size >= 1

        total = len(self.indexed_dataset().keys())
        last_key = sorted(self.indexed_dataset().keys())[-1]
        i, data = index, []

        # Skip over deleted keys
        while i < last_key and len(data) < page_size:
            val = self.indexed_dataset().get(i)
            if val:
                data.append(val)
            i += 1
        return {
            'index': index,
            'next_index': i if total >= i else None,
            'page_size': len(data),
            'data': data
        }


if __name__ == '__main__':
    """Tests the code in this module"""
    server = Server()

    server.indexed_dataset()

    try:
        server.get_hyper_index(300000, 100)
    except AssertionError:
        print("AssertionError raised when out of range")

    index = 3
    page_size = 2

    print("Number of items: {}".format(len(server._Server__indexed_dataset)))
    print('\nindex = 3, page_size = 2 -> server.get_hyper_index(3, 2)')

    print('\n1. Request first index')
    res = server.get_hyper_index(index, page_size)
    print(res)

    print('\n2. Request next index')
    print(server.get_hyper_index(res.get('next_index'), page_size))

    print('\n3. Remove the first index -> ', end='')
    del server._Server__indexed_dataset[res.get('index')]
    print("Number of items: {}".format(len(server._Server__indexed_dataset)))

    print('\n4. Redo 1. -> First item in data should have changed')
    print(server.get_hyper_index(index, page_size))

    print('\n5. Redo 2. -> Data should be identical')
    print(server.get_hyper_index(res.get('next_index'), page_size))
