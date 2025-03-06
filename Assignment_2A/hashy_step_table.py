""" Hash Table ADT

Defines a Hash Table using a modified Linear Probe implementation for conflict resolution.
"""
from __future__ import annotations
__author__ = 'Jackson Goerner'
__since__ = '07/02/2023'

from data_structures.referential_array import ArrayR
from typing import Generic, TypeVar, Union

K = TypeVar('K')
V = TypeVar('V')


class FullError(Exception):
    pass


class HashyStepTable(Generic[K, V]):
    """
    Hashy Step Table.

    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise `hash` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869]

    HASH_BASE = 31

    DELETED = object()  # Sentinel for deleted slots

    def __init__(self, sizes=None) -> None:
        """
        Initialise the Hash Table.

        Complexity:
        Best Case Complexity: O(max(N, M)) where N is the length of TABLE_SIZES and M is the length of sizes.
        Worst Case Complexity: O(max(N, M)) where N is the length of TABLE_SIZES and M is the length of sizes.
        """
        if sizes is not None:
            self.TABLE_SIZES = sizes
        self.size_index = 0
        self.array: ArrayR[Union[tuple[K, V], None]] = ArrayR(self.TABLE_SIZES[self.size_index])
        self.count = 0

    def hash(self, key: K) -> int:
        """
        Hash a key for insert/retrieve/update into the hashtable.

        Complexity:
        Best Case Complexity: O(len(key))
        Worst Case Complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: K) -> int:
        """
        Used to determine the step size for our hash table.

        Complexity: 4n + 2, where n is the length of the key
        Best Case Complexity: O(n) where n is the length of the key
        Worst Case Complexity: O(n) where n is the length of the key
        """
        value = 0
        for char in key:
            value = (ord(char) + value * 37) % self.table_size  # Use a different base than hash
        return max(1, value)  # Ensure step size is at least 1

    @property
    def table_size(self) -> int:
        return len(self.array)

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        """
        return self.count

    def _hashy_probe(self, key: K, is_insert: bool) -> int:
        """
        Find the correct position for this key in the hash table using hashy probing.

        Raises:
        KeyError: When the key is not in the table, but is_insert is False.
        FullError: When a table is full and cannot be inserted.

        Complexity: 2h + 1 + m(3 + n), where h is num of operations in each hash, n is the length of the key, m is the
                                        size of the hash table
        Best Case Complexity: O(n), where n is the length of the key
        Worst Case Complexity: O(m * n), where n is the length of the key, m is the length of the hash table
        """
        # Initial position
        position = self.hash(key)
        step_size = self.hash2(key)
        first_deleted = None  # To keep track of the first deleted slot

        for _ in range(self.table_size):
            if self.array[position] is None:
                if is_insert:
                    return first_deleted if first_deleted is not None else position
                else:
                    # Key not found
                    raise KeyError(f"Key {key} not found")
            elif self.array[position] == self.DELETED:
                # Keep track of the first deleted slot
                if first_deleted is None:
                    first_deleted = position
                # Continue probing
            elif self.array[position][0] == key:
                # Key found
                return position
            # Else, continue probing

            # Move to the next slot
            position = (position + step_size) % self.table_size

        if is_insert and first_deleted is not None:
            return first_deleted
        elif is_insert:
            raise FullError("Hash table is full")
        else:
            raise KeyError(f"Key {key} not found")
    
    def keys(self) -> list[K]:
        """
        Returns all keys in the hash table.

        :complexity: O(N) where N is self.table_size.
        """
        res = []
        for x in range(self.table_size):
            if self.array[x] is not None:
                res.append(self.array[x][0])
        return res

    def values(self) -> list[V]:
        """
        Returns all values in the hash table.

        :complexity: O(N) where N is self.table_size.
        """
        res = []
        for x in range(self.table_size):
            if self.array[x] is not None:
                res.append(self.array[x][1])
        return res

    def __contains__(self, key: K) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See hashy probe.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :complexity: See hashy probe.
        :raises KeyError: when the key doesn't exist.
        """
        position = self._hashy_probe(key, False)
        return self.array[position][1]

    def __setitem__(self, key: K, data: V) -> None:
        """
        Set an (key, value) pair in our hash table.

        :complexity: See hashy probe.
        :raises FullError: when the table cannot be resized further.
        """

        position = self._hashy_probe(key, True)

        if self.array[position] is None:
            self.count += 1

        self.array[position] = (key, data)

        if len(self) > self.table_size * 2 / 3:
            self._rehash()

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) using lazy deletion

        Complexity: k(n + 2) + 2, where k is number of positions probed, and n is length of the key
        Best Case Complexity: O(1)
        Worst Case Complexity: O(m * n) where n is length of key, m is size of the hash table
        """
        position = self._hashy_probe(key, False)
        self.array[position] = self.DELETED  # Mark as deleted with sentinel
        self.count -= 1

    def is_empty(self) -> bool:
        return self.count == 0

    def is_full(self) -> bool:
        return self.count == self.table_size

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        Complexity:
        Best Case Complexity:
        Worst Case Complexity:
        """
        old_array = self.array
        self.size_index += 1
        if self.size_index >= len(self.TABLE_SIZES):
            raise FullError("Cannot resize table further")

        self.array = ArrayR(self.TABLE_SIZES[self.size_index])  # New larger table
        self.count = 0  # Reset count

        for item in old_array:
            if item is not None:
                key, value = item
                self[key] = value  # Reinsert into the new table

    def __str__(self) -> str:
        """
        Returns all they key/value pairs in our hash table (no particular
        order).
        :complexity: O(N * (str(key) + str(value))) where N is the table size
        """
        result = ""
        for item in self.array:
            if item is not None:
                (key, value) = item
                result += "(" + str(key) + "," + str(value) + ")\n"
        return result
