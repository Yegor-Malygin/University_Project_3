from __future__ import annotations
from data_structures.bset import BSet
from data_structures.referential_array import ArrayR
from data_structures.array_sorted_list import ArraySortedList
from data_structures.linked_list import LinkedList
from dataclasses import dataclass
from team import Team
from typing import Generator, Union
from constants import Constants, TeamStats, PlayerStats
from game_simulator import GameSimulator


@dataclass
class Game:
    """
    Simple container for a game between two teams.
    Both teams must be team objects, there cannot be a game without two teams.

    Note: Python will automatically generate the init for you.
    Use Game(home_team: Team, away_team: Team) to use this class.
    See: https://docs.python.org/3/library/dataclasses.html
    """
    home_team: Team = None
    away_team: Team = None


class WeekOfGames:
    """
    Simple container for a week of games.

    A fixture must have at least one game.
    """

    def __init__(self, week: int, games: ArrayR[Game]) -> None:
        """
        Container for a week of games.

        Args:
            week (int): The week number.
            games (ArrayR[Game]): The games for this week.
        """
        self.games: ArrayR[Game] = games
        self.week: int = week

    def get_games(self) -> ArrayR:
        """
        Returns the games in a given week.

        Returns:
            ArrayR: The games in a given week.

        Complexity:
        Best Case Complexity: O(1)
        Worst Case Complexity: O(1)
        """
        return self.games

    def get_week(self) -> int:
        """
        Returns the week number.

        Returns:
            int: The week number.

        Complexity:
        Best Case Complexity: O(1)
        Worst Case Complexity: O(1)
        """
        return self.week

    def __iter__(self):
        """
        Complexity:
        Best Case Complexity:
        Worst Case Complexity:
        """
        raise NotImplementedError

    def __next__(self):
        """
        Complexity:
        Best Case Complexity:
        Worst Case Complexity:
        """
        raise NotImplementedError


class Season:

    def __init__(self, teams: ArrayR[Team]) -> None:
        """
        Initializes the season with a schedule.

        Args:
            teams (ArrayR[Team]): The teams played in this season.

        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        self.leaderboard = ArraySortedList(Constants.MAX_NUM_TEAMS)
        self.schedule = LinkedList()
        self.teams = teams
        self.generated_schedule = self._generate_schedule()
        for item in self.generated_schedule:
            self.schedule.append(item)

        for team in self.teams:
            self.leaderboard.add(team)

    def _generate_schedule(self) -> ArrayR[ArrayR[Game]]:
        """
        Generates a schedule by generating all possible games between the teams.

        Return:
            ArrayR[ArrayR[Game]]: The schedule of the season.
                The outer array is the weeks in the season.
                The inner array is the games for that given week.

        Complexity:
            Best Case Complexity: O(N^2) where N is the number of teams in the season.
            Worst Case Complexity: O(N^2) where N is the number of teams in the season.
        """
        num_teams: int = len(self.teams)
        weekly_games: list[ArrayR[Game]] = []
        flipped_weeks: list[ArrayR[Game]] = []
        games: list[Game] = []

        # Generate all possible matchups (team1 vs team2, team2 vs team1, etc.)
        for i in range(num_teams):
            for j in range(i + 1, num_teams):
                games.append(Game(self.teams[i], self.teams[j]))

        # Allocate games into each week ensuring no team plays more than once in a week
        week: int = 0
        while games:
            current_week: list[Game] = []
            flipped_week: list[Game] = []
            used_teams: BSet = BSet()

            week_game_no: int = 0
            for game in games[:]:  # Iterate over a copy of the list
                if game.home_team.get_number() not in used_teams and game.away_team.get_number() not in used_teams:
                    current_week.append(game)
                    used_teams.add(game.home_team.get_number())
                    used_teams.add(game.away_team.get_number())

                    flipped_week.append(Game(game.away_team, game.home_team))
                    games.remove(game)
                    week_game_no += 1

            weekly_games.append(ArrayR.from_list(current_week))
            flipped_weeks.append(ArrayR.from_list(flipped_week))
            week += 1

        return ArrayR.from_list(weekly_games + flipped_weeks)

    def simulate_season(self) -> None:
        """
        Simulates the season.

        Complexity:
            Assume simulate_game is O(1)
            Remember to define your variables and their complexity.

            Best Case Complexity: O(n^2 + m + g) where n is the number of player in the teams, m is the length of half of
                                    the schedule, g is the number of game in the schedule
            Worst Case Complexity: O(n^2 + m + g)
        """
        final_temp_schedule_1 = LinkedList()
        final_temp_schedule_2 = LinkedList()
        # generate schedule gave it to me in a weird order, where it is g1 w1, then g1 w2, g1 w3, g2 w3, g2 w2 etc.
        # and i wrote this loop to sort it out correctly, only to realise that the test cases wanted the initially
        # sorted list, if it was initially sorted in this way, all other operations would be simpler and more robust
        # spent too much time doing this and made all of task 5 work before changing everything for task 4
        # at this point ill be happy with above 50% because the generate schedule function is just down right stupid
        # unless i missed something
        temp_schedule = self.generated_schedule[0: len(self.generated_schedule) // 2]
        iterator = len(temp_schedule) // 2
        for game in range(len(temp_schedule)):
            if game < len(temp_schedule) // 2:
                final_temp_schedule_1.append(temp_schedule[game])
            else:
                final_temp_schedule_1.insert(iterator, temp_schedule[game])
                iterator = iterator - 1

        # loop for second half (flipped) schedule
        temp_schedule = self.generated_schedule[len(self.generated_schedule) // 2: len(self.generated_schedule)]
        iterator = len(temp_schedule) // 2
        for game in range(len(temp_schedule)):
            if game < len(temp_schedule) // 2:
                final_temp_schedule_2.append(temp_schedule[game])
            else:
                final_temp_schedule_2.insert(iterator, temp_schedule[game])
                iterator = iterator - 1

        self.schedule.clear()
        for item in final_temp_schedule_1:
            self.schedule.append(item)
        for item in final_temp_schedule_2:
            self.schedule.append(item)

        # wrote a function for repeated lines of code
        def update_player_stats(key, played_game, game, stat):
            if played_game[key] is None:
                return None
            else:
                # for every player given in the input
                for player in played_game[key]:
                    # for every player in the home team
                    for person in game[0].home_team.get_players():
                        # if the players name matches the player we are looking for, adjust that players statistic
                        if player == person.name:
                            person[stat] += 1
                    # for every player in the away team
                    for person in game[0].away_team.get_players():
                        if player == person.name:
                            person[stat] += 1

        # iterate through every game within the schedule
        for game in self.schedule:

            # simulate the game
            played_game = GameSimulator.simulate(game[0].home_team, game[0].away_team)

            # go through the goals to determine whether it was a win, loss or draw
            if played_game["Home Goals"] > played_game["Away Goals"]:
                game[0].home_team[TeamStats.WINS] += 1
                game[0].away_team[TeamStats.LOSSES] += 1
            elif played_game["Home Goals"] < played_game["Away Goals"]:
                game[0].away_team[TeamStats.WINS] += 1
                game[0].home_team[TeamStats.LOSSES] += 1
            else:
                game[0].away_team[TeamStats.DRAWS] += 1
                game[0].home_team[TeamStats.DRAWS] += 1

            # go through every player in each of the teams and adjust their games played stat
            for position in game[0].home_team.players:
                for player in position:
                    player[PlayerStats.GAMES_PLAYED] += 1

            for position in game[0].away_team.players:
                for player in position:
                    player[PlayerStats.GAMES_PLAYED] += 1

            # go through every key in the played game class
            for key in played_game.keys():
                # adjust goals for and against for each of the teams
                if key == "Home Goals":
                    game[0].home_team[TeamStats.GOALS_FOR] += played_game["Home Goals"]
                    game[0].away_team[TeamStats.GOALS_AGAINST] += played_game["Home Goals"]
                elif key == "Away Goals":
                    game[0].away_team[TeamStats.GOALS_FOR] += played_game["Away Goals"]
                    game[0].home_team[TeamStats.GOALS_AGAINST] += played_game["Away Goals"]

                # go through every player mentioned in the played game instance and adjust the relevant statistics
                elif key == "Goal Scorers":
                    update_player_stats(key, played_game, game, PlayerStats.GOALS)
                elif key == "Interceptions":
                    update_player_stats(key, played_game, game, PlayerStats.INTERCEPTIONS)
                elif key == "Tackles":
                    update_player_stats(key, played_game, game, PlayerStats.TACKLES)
                else:
                    update_player_stats(key, played_game, game, PlayerStats.ASSISTS)

    def delay_week_of_games(self, orig_week: int, new_week: Union[int, None] = None) -> None:
        """
        Delay a week of games from one week to another.

        Args:
            orig_week (int): The original week to move the games from.
            new_week (Union[int, None]): The new week to move the games to. If this is None, it moves the games to the end of the season.

        Complexity:
            Best Case Complexity: O(n) for the number of games played per week
            Worst Case Complexity: O(n) for the number of games played per week
        """
        games_per_week = len(self.teams) // 2
        delayed_games_list = []
        # if the schedule was initially sorted in an easier to understand format, the following code could've been used
        # and would have probably been more robust
        """the following code works for the properly sorted list of games e.g. w1g1 w1g2 w2g1 w2g2 etc.
        but mine always sorted it w1g1 w2g1 w3g1 w3g2 w2g2 w1g2 so thats why i implemented the other code 
        games_iterator = 1
        for _ in range(games_per_week):
            delayed_games_list.append(self.schedule[(orig_week * games_per_week) - games_iterator])
            self.schedule.delete_at_index((orig_week * games_per_week) - games_iterator)
            games_iterator -= 1
        if new_week is None:
            for game in delayed_games_list:
                self.schedule.append(game)
        else:
            insertion_index = new_week * games_per_week
            for game in delayed_games_list:
                self.schedule.insert(insertion_index, game)
                insertion_index += 1
        """

        length_of_schedule = len(self.schedule)
        if orig_week <= length_of_schedule // 4:
            delayed_games_list.append(self.schedule[orig_week - 1])
            delayed_games_list.append(self.schedule[length_of_schedule // 2 - (orig_week - 1)])
            self.schedule.delete_at_index(orig_week - 1)
            self.schedule.delete_at_index(length_of_schedule // 2 - orig_week - 1)
        else:
            delayed_games_list.append(self.schedule[length_of_schedule // 2 + (orig_week - length_of_schedule // 4) - 1])
            delayed_games_list.append(self.schedule[length_of_schedule - (orig_week - length_of_schedule // 4)])
            self.schedule.delete_at_index(length_of_schedule // 2 + (orig_week - length_of_schedule // 4) - 1)
            self.schedule.delete_at_index(length_of_schedule - (orig_week - length_of_schedule // 4))

        if new_week is None:
            iterator = -4
            for game in delayed_games_list:
                self.schedule.insert(((length_of_schedule // 4) * 3) + iterator, game)
                iterator = iterator + 1
        else:
            length_of_schedule = len(self.schedule)
            self.schedule.insert(length_of_schedule // 2 + (orig_week - length_of_schedule // 4) - 2, delayed_games_list[0])
            self.schedule.insert(length_of_schedule - (orig_week - length_of_schedule // 4), delayed_games_list[1])


    def get_next_game(self) -> Union[Generator[Game], None]:
        """
        Gets the next game in the season.

        Returns:
            Game: The next game in the season.
            or None if there are no more games left.

        Complexity:
            Best Case Complexity: O(1) if schedule is empty
            Worst Case Complexity: O(1) if schedule is not empty
        """
        if self.schedule.is_empty():
            return None

        next_game = self.schedule[0]
        self.schedule.delete_at_index(0)
        return next_game

    def get_leaderboard(self) -> ArrayR[ArrayR[Union[int, str]]]:
        """
        Generates the final season leaderboard.

        Returns:
            ArrayR(ArrayR[ArrayR[Union[int, str]]]):
                Outer array represents each team in the leaderboard
                Inner array consists of 10 elements:
                    - Team name (str)
                    - Games Played (int)
                    - Points (int)
                    - Wins (int)
                    - Draws (int)
                    - Losses (int)
                    - Goals For (int)
                    - Goals Against (int)
                    - Goal Difference (int)
                    - Previous Five Results (ArrayR(str)) where result should be WIN LOSS OR DRAW

        Complexity:
            Best Case Complexity: O(n) where n is the number of teams
            Worst Case Complexity: O(n) where n is the number of teams
        """
        leaderboard_disp = ArrayR(len(self.teams))
        team_iterator = 0
        # go through every team belonging the self.teams
        for team in self.leaderboard:
            stats = ArrayR(len(TeamStats) + 1)
            stats[0] = team.name
            stats[1] = team[TeamStats.GAMES_PLAYED]
            stats[2] = team[TeamStats.POINTS]
            stats[3] = team[TeamStats.WINS]
            stats[4] = team[TeamStats.DRAWS]
            stats[5] = team[TeamStats.LOSSES]
            stats[6] = team[TeamStats.GOALS_FOR]
            stats[7] = team[TeamStats.GOALS_AGAINST]
            stats[8] = team[TeamStats.GOALS_DIFFERENCE]
            stats[9] = team[TeamStats.LAST_FIVE_RESULTS]
            # if the current team has more points than the previous team, switch them around
            if team_iterator > 0 and stats[2] > leaderboard_disp[team_iterator - 1][2]:
                temp = leaderboard_disp[team_iterator - 1]
                leaderboard_disp[team_iterator - 1] = stats
                leaderboard_disp[team_iterator] = temp
            # otherwise just append this to the end of the leaderboard
            else:
                leaderboard_disp[team_iterator] = stats
            team_iterator += 1

        return leaderboard_disp





    def get_teams(self) -> ArrayR[Team]:
        """
        Returns:
            PlayerPosition (ArrayR(Team)): The teams participating in the season.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return self.teams

    def __len__(self) -> int:
        """
        Returns the number of teams in the season.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return len(self.teams)

    def __str__(self) -> str:
        """
        Optional but highly recommended.

        You may choose to implement this method to help you debug.
        However your code must not rely on this method for its functionality.

        Returns:
            str: The string representation of the season object.

        Complexity:
            Analysis not required.
        """
        return ""

    def __repr__(self) -> str:
        """Returns a string representation of the Season object.
        Useful for debugging or when the Season is held in another data structure."""
        return str(self)
