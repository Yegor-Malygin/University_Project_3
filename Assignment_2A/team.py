from __future__ import annotations

import constants
from data_structures.referential_array import ArrayR
from constants import Constants, GameResult, PlayerPosition, PlayerStats, TeamStats
from player import Player
from typing import Collection, Union, TypeVar
from data_structures.hash_table_separate_chaining import HashTableSeparateChaining
from data_structures.linked_queue import LinkedQueue
from data_structures.linked_list import LinkedList

T = TypeVar("T")


class Team:
    # set a class variable, and adjust it every time an instance of the class if made
    team_number = 0

    def __init__(self, team_name: str, players: ArrayR[Player]) -> None:
        """
        Constructor for the Team class

        Args:
            team_name (str): The name of the team
            players (ArrayR[Player]): The players of the team

        Returns:
            None

        Complexity:
            Best Case Complexity: O(n) where n is number if players
            Worst Case Complexity: O(n) where n is number of players
        """
        # set team number to the class variable
        self.team_number = Team.team_number + 1
        self.name = team_name
        self.statistics = HashTableSeparateChaining(Constants.MAX_NUM_TEAMS)

        # go through every item in the team statistics
        for item in TeamStats.__members__:
            # if it is the statistic for the last five results, enter a linked queue instead
            if item == "LAST_FIVE_RESULTS":
                last_five_results = LinkedQueue()
                self.statistics.insert(item, last_five_results)
            else:
                self.statistics.insert(item, 0)

        self.players = HashTableSeparateChaining(Constants.TEAM_MAX_PLAYERS)
        # inside the hash table, create the 4 keys for each of the positions, with an empty list for values
        for position in constants.PlayerPosition:
            self.players.insert(position.name, [])

        # go through every player and add them to the hash table values accordingly
        for player in players:
            if player.get_position().name in self.players.keys():
                self.players[player.get_position().name].append(player)

    def reset_stats(self) -> None:
        """
        Resets all the statistics of the team to the values they were during init.

        Complexity:
            Best Case Complexity: O(1) since we have a known number of stats
            Worst Case Complexity: O(1)
        """
        for stat in self.statistics.keys():
            if stat == "LAST_FIVE_RESULTS":
                self.statistics[stat].clear()
            else:
                self.statistics.insert(stat, 0)

    def add_player(self, player: Player) -> None:
        """
        Adds a player to the team.

        Args:
            player (Player): The player to add

        Returns:
            None

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        self.players[player.get_position().name].append(player)

    def remove_player(self, player: Player) -> None:
        """
        Removes a player from the team.

        Args:
            player (Player): The player to remove

        Returns:
            None

        Complexity:
            Best Case Complexity: O(n) where n is the number of players (since we have a known number of positions)
            Worst Case Complexity: O(n) where n is the number of players (since we have a known number of positions)
        """
        # go through every position
        for position in self.players.keys():
            if position == player.get_position().name:
                # go through every person in the positions list, and if they match to the given player, remove them
                for person in self.players[position]:
                    if person == player:
                        self.players[position].remove(person)

    def get_number(self) -> int:
        """
        Returns the number of the team.

        Complexity:
            Analysis not required.
        """
        return self.team_number

    def get_name(self) -> str:
        """
        Returns the name of the team.

        Complexity:
            Analysis not required.
        """
        return self.name

    def get_players(self, position: Union[PlayerPosition, None] = None) -> Union[Collection[Player], None]:
        """
        Returns the players of the team that play in the specified position.
        If position is None, it should return ALL players in the team.
        You may assume the position will always be valid.
        Args:
            position (Union[PlayerPosition, None]): The position of the players to return

        Returns:
            Collection[Player]: The players that play in the specified position
            held in a valid data structure provided to you within
            the data_structures folder this includes the ArrayR
            which was previously prohibited.

            None: When no players match the criteria / team has no players

        Complexity:
            Best Case Complexity: O(n) where n is the number of players in a position
            Worst Case Complexity: O(n) where n is the number of players in the team
        """
        collection = LinkedList()

        # if we are given a position
        if position is not None:
            if position.name in self.players.keys():
                # for every player in the given position, add it to collection
                for player in self.players[position.name]:
                    collection.append(player)
        else:
            for player in self.players["GOALKEEPER"]:
                collection.append(player)
            for player in self.players["DEFENDER"]:
                collection.append(player)
            for player in self.players["MIDFIELDER"]:
                collection.append(player)
            for player in self.players["STRIKER"]:
                collection.append(player)

        if collection.is_empty():
            return None

        return collection

    def get_statistics(self):
        """
        Get the statistics of the team

        Returns:
            statistics: The teams' statistics

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return self.statistics

    def get_last_five_results(self) -> Union[Collection[GameResult], None]:
        """
        Returns the last five results of the team.
        If the team has played less than five games,
        return all the result of all the games played so far.

        For example:
        If a team has only played 4 games and they have:
        Won the first, lost the second and third, and drawn the last,
        the array should be an array of size 4
        [GameResult.WIN, GameResult.LOSS, GameResult.LOSS, GameResult.DRAW]

        **Important Note:**
        If this method is called before the team has played any games,
        return None the reason for this is explained in the specefication.

        Returns:
            Collection[GameResult]: The last five results of the team
            or
            None if the team has not played any games.

        Complexity:
            Best Case Complexity: O(1) if the team has not played any games
            Worst Case Complexity: O(1) since the length of last five results will not be longer than 5
        """

        if len(self.statistics["LAST_FIVE_RESULTS"]) == 0:
            return None

        return_list = LinkedList()
        operations_list = self.statistics["LAST_FIVE_RESULTS"]

        for _ in range(len(operations_list)):
            item = operations_list.serve()
            return_list.append(item)
            operations_list.append(item)

        return return_list

    def get_top_x_players(self, player_stat: PlayerStats, num_players: int) -> list[tuple[int, str, Player]]:
        """
        Note: This method is only required for FIT1054 students only!

        Args:
            player_stat (PlayerStats): The player statistic to use to order the top players
            num_players (int): The number of players to return from this team

        Return:
            list[tuple[int, str, Player]]: The top x players from this team
        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        raise NotImplementedError

    def __setitem__(self, statistic: TeamStats, value: int) -> None:
        """
        Updates the team's statistics.

        Args:
            statistic (TeamStats): The statistic to update
            value (int): The new value of the statistic

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        self.statistics[statistic.name] = value
        if statistic.name == "WINS" or statistic.name == "LOSSES" or statistic.name == "DRAWS":
            self.statistics["GAMES_PLAYED"] += 1
            if statistic.name == "WINS":
                self.statistics["POINTS"] += GameResult.WIN
                self.statistics["LAST_FIVE_RESULTS"].append(GameResult.WIN)
            elif statistic.name == "DRAWS":
                self.statistics["POINTS"] += GameResult.DRAW
                self.statistics["LAST_FIVE_RESULTS"].append(GameResult.DRAW)
            else:
                self.statistics["LAST_FIVE_RESULTS"].append(GameResult.LOSS)
            if len(self.statistics["LAST_FIVE_RESULTS"]) > 5:
                self.statistics["LAST_FIVE_RESULTS"].serve()
        if statistic.name == "GOALS_FOR" or statistic.name == "GOALS_AGAINST":
            self.statistics["GOALS_DIFFERENCE"] = self.statistics["GOALS_FOR"] - self.statistics["GOALS_AGAINST"]

    def __getitem__(self, statistic: TeamStats) -> int:
        """
        Returns the value of the specified statistic.

        Args:
            statistic (TeamStats): The statistic to return

        Returns:
            int: The value of the specified statistic

        Raises:
            ValueError: If the statistic is invalid

        Complexity:
            Best Case Complexity: O(1) if the item is in the first position in the list
            Worst Case Complexity: O(n) where n is the position of the item we are looking for
        """
        return self.statistics[statistic.name]

    def __len__(self) -> int:
        """
        Returns the number of players in the team.

        Complexity:
            Best Case Complexity: O(n) where n is the number of players
            Worst Case Complexity: O(n) where n is the number of players
        """
        count_of_players = 0

        # go through every position
        for position in self.players.keys():
            # go through every player in that position
            for player in self.players[position]:
                count_of_players += 1

        return count_of_players

    def __gt__(self, other):
        """
        Returns the greater than boolean

        Complexity:
            Best Case Complexity: O(n) where n is the number of letter in the key with less letter
            Worst Case Complexity: O(n) where n is the number of letters in the keys
        """
        if len(self.name) > len(other.name):
            length = len(other.name)
        else:
            length = len(self.name)

        for letter in range(length):
            if ord(self.name[letter]) == ord(other.name[letter]):
                continue
            else:
                return ord(self.name[letter]) > ord(other.name[letter])

    def __lt__(self, other):
        """
        Returns the less than boolean

        Complexity:
            Best Case Complexity: O(n) where n is the number of letter in the key with less letter
            Worst Case Complexity: O(n) where n is the number of letters in the keys
        """
        if len(self.name) > len(other.name):
            length = len(other.name)
        else:
            length = len(self.name)

        for letter in range(length):
            if ord(self.name[letter]) == ord(other.name[letter]):
                continue
            else:
                return ord(self.name[letter]) < ord(other.name[letter])

    def __str__(self) -> str:
        """
        Optional but highly recommended.

        You may choose to implement this method to help you debug.
        However your code must not rely on this method for its functionality.

        Returns:
            str: The string representation of the team object.

        Complexity:
            Analysis not required.
        """
        return self.name

    def __repr__(self) -> str:
        """Returns a string representation of the Team object.
        Useful for debugging or when the Team is held in another data structure."""
        return str(self)
