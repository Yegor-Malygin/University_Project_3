from __future__ import annotations
from constants import PlayerPosition, PlayerStats
from data_structures.hash_table_separate_chaining import HashTableSeparateChaining


class Player:

    def __init__(self, name: str, position: PlayerPosition, age: int) -> None:
        """
        Constructor for the Player class

        Args:
            name (str): The name of the player
            position (PlayerPosition): The position of the player
            age (int): The age of the player

        Returns:
            None

        Complexity:
            Best Case Complexity: O(1) since we have a fixed number of player statistics
            Worst Case Complexity: O(1) since we have a fixed number of player statistics

        """
        table_length = len(PlayerStats.__members__)
        self.name = name
        self.position = position
        self.age = age
        self.statistics = HashTableSeparateChaining(table_length)

        # __members__ basically gives us all odf the keys or elements within the class
        for item in PlayerStats.__members__:
            self.statistics.insert(item, 0)

    def reset_stats(self) -> None:
        """
        Reset the stats of the player

        Returns:
            None

        Complexity:
            Best Case Complexity: O(1) since we have a fixed number of player statistics
            Worst Case Complexity: O(1) since we have a fixed number of player statistics

        """
        # go through every element in the hash table and reset the value to 0
        for statistic in self.statistics.keys():
            self.statistics[statistic] = 0

    def get_name(self) -> str:
        """
        Get the name of the player

        Returns:
            str: The name of the player

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return self.name

    def get_position(self) -> PlayerPosition:
        """
        Get the position of the player

        Returns:
            PlayerPosition: The position of the player

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return self.position

    def get_statistics(self):
        """
        Get the statistics of the player

        Returns:
            statistics: The players' statistics

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return self.statistics

    def __setitem__(self, statistic: PlayerStats, value: int) -> None:
        """
        Set the value of the player's stat based on the key that is passed.

        Args:
            statistic (PlayerStat): The key of the stat
            value (int): The value of the stat

        Returns:
            None

        Complexity:
            Best Case Complexity: O(1) if the hash table is empty
            Worst Case Complexity: O(n) where n is the number of items in the hash table, in the case of
                                    updating values
        """
        self.statistics[statistic.name] = value

    def __getitem__(self, statistic: PlayerStats) -> int:
        """
        Get the value of the player's stat based on the key that is passed.

        Args:
            statistic (PlayerStat): The key of the stat

        Returns:
            int: The value of the stat

        Complexity:
            Best Case Complexity: O(1) if the element is at the front of the hash table
            Worst Case Complexity: O(n) where n is the position of the item being searched for
        """
        return self.statistics[statistic.name]

    def __str__(self) -> str:
        """
        Optional but highly recommended.

        You may choose to implement this method to help you debug.
        However your code must not rely on this method for its functionality.

        Returns:
            str: The string representation of the player object.

        Complexity:
            Analysis not required.
        """
        return f"{self.name} {self.position}"

    def __repr__(self) -> str:
        """Returns a string representation of the Player object.
        Useful for debugging or when the Player is held in another data structure."""
        return str(self)
