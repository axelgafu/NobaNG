import settings
import pygame
import player as player_module

from typing import Sequence
from player import Character, Player
from random import randint

# seed(2022-2-10)
#
# Class: GameData
# ==============================================================================


class GameData:
    """Holds game state meta-data.

    This class represents the overall game moderator and it is updated by the
    game states.
    """

    _instance = None

    def __call__(self, *args, **kwargs):
        """Implements Singleton design pattern from
        `refactoring.guru
        <https://refactoring.guru/es/design-patterns/singleton/python/example>`
        """
        if self._instance is None:
            self._instance = super().__call__(*args, **kwargs)

        return self._instance

    def __init__(self):
        """Initializes the data that is to be used during the Game.
        This class implements the singleton design pattern to keep consistency
        throughout the game.
        """
        self.keys = None
        self._player_list = {}
        self._player_head = None
        self._current_player = None
        self.arrows_left = settings.MAX_ARROWS_COUNT
        pygame.key.set_repeat(0)

    def player_list(self) -> list:
        """Returns a `list` of `Player` objects where each element represents
        one of the players in the game.
        """
        return list(self._player_list.values())

    def next_player(self) -> Player:
        """Returns a `Player` object with the information of the **next** player.
        Calling this function moves game state to the next player.
        """
        if self._current_player is not None:
            self._current_player = self._current_player.right_hand_player
        else:
            self._current_player = self._player_head

        return self._current_player

    def current_player(self) -> Player:
        """Returns a `Player` object with the information of **current** player.
        Calling this function does not change game state.
        """
        if self._current_player is None:
            self._current_player = self._player_head

        return self._current_player

    def update_keys(self, keys: Sequence):
        """Use this function to read user input.
        User input is read from keyboard and it is read one key at a time. Each
        input is processed against the game state. Depending on the input, game
        state may change or not.

        For more information about how user input may change game state, please
        refer to the specific game states (`State` class)
        """
        self.keys = keys

    def append_player(self, player: Player):
        """Adds a new player to the game room."""
        if player.name not in self._player_list.keys():
            if self._player_head is not None:
                player.left_hand_player = self._player_head

                player.right_hand_player = self._player_head.right_hand_player
                self._player_head.right_hand_player = player

            self._player_list[player.name] = player
            self._player_head = player

    def players_count(self) -> int:
        """Returns an `int` that represents how many players are in the game."""
        return len(self._player_list)

    def is_first_death(self) -> bool:
        """This function returns True when only a single player has status
        equals to ``Player.S_DEAD``
        """
        counts = [player.status for player in self.player_list()]

        return counts.count("dead") == 1


class GameRules:
    """This class is intended to hold all the algorithms that rule the game
    interactions with game players.
    """

    _instance = None

    def __call__(self, *args, **kwargs):
        """Implements Singleton design pattern from
        `refactoring.guru
        <https://refactoring.guru/es/design-patterns/singleton/python/example>`
        """
        if self._instance is None:
            self._instance = super().__call__(*args, **kwargs)

        return self._instance

    def __init__(self) -> None:
        """Initializes the game rules.
        This class implements the singleton design pattern.
        """
        self._dice_list = {
            "regular": ["1", "2", "shoot", "arrow", "bomb", "life"],
            "brave": ["2x1", "2x2", "bomb", "arrow", "shoot", "bullet"],
            "coward": ["1", "no_arrow", "bomb", "arrow", "2xlife", "life"],
        }

    def visit_assign_character(self, player: Player):
        """Randomly assign a character to the given player."""
        characters = [c for c in Character.__subclasses__()]
        options = len(characters) - 1

        # Load class from name
        class_name = characters[randint(0, options)].__name__
        clazz = getattr(player_module, class_name)
        player.character = clazz()

    def visit_initialize_player(self, player: Player):
        """Applies the boosts and effects of the assigned character and role
        to the given player"""
        if player.character is not None:
            player.character.initialize(player)

    def visit_throw_dice(self, player: Player, brave: bool) -> bool:
        """Update player statistics based on dice rule.
        :return: True if player's turn ends.

        .. note::
            **Rule**
            If player is alive, use `throw_alive`.
            If plaier is ghost, use `throw_ghost`.
        """
        if player.status == "ghost":
            self.throw_ghost(player)
        else:
            self.throw_alive(player, brave)

        return False

    def throw_alive(self, player: Player, brave):
        """Update player statistics based on alive dice rule.
        :return: True if player's turn ends.

        .. note::
            **Rule**
            Throw dice with full character capacity.
        """
        if player.dice_re_roll[0] > 0:
            if brave:
                player.dice_value[0] = self._dice_list["brave"][randint(0, 5)]
            else:
                player.dice_value[0] = self._dice_list["coward"][randint(0, 5)]
            player.dice_re_roll[0] -= 1

        for i in range(1, player.dice_count):
            if player.dice_re_roll[i] > 0:
                player.dice_re_roll[i] -= 1
                player.dice_value[i] = self._dice_list["regular"][randint(
                    0, 5)]
                if player.dice_value[i] == "bomb":
                    player.dice_re_roll[i] = 0

    def throw_ghost(self, player: Player):
        """Update player statistics based on alive dice rule.
        :return: True if player's turn ends.

        .. note::
            **Rule**
            Throw just 2 dice.
        """
        for i in range(0, 1):
            if player.dice_re_roll[i] > 0:
                player.dice_re_roll[0] -= 1
                player.dice_value[i] = self._dice_list["regular"][randint(
                    0, 5)]
                if player.dice_value[i] == "bomb":
                    player.dice_re_roll[i] = 0

    def visit_life(self, player: Player) -> bool:
        """Update player statistics based on life rule.
        :return: True if player's turn ends.

        .. note::
            **Rule**
            Whenever it is within the character limits:
             - If '2xlife' is obtained player gains two life points.
             - If 'life' is obtained player gains one life points.
        """
        counts = {i: player.dice_value.count(i) for i in player.dice_value}

        if "2xlife" in counts.keys():
            player.life += 2 * counts["2xlife"]

        if "life" in counts.keys():
            player.life += counts["life"]

        player.life = min(player.max_life, player.life)
        return False

    def visit_character_stats_rules(self, player: Player) -> bool:
        player.character.visit_character_stats_rules(player)

        return False

    def visit_character_counter_rules(self, game_data: GameData) -> bool:
        player: Player = game_data.current_player()
        player.character.visit_character_counter_rules(game_data, self)

        return False

    def visit_bombs(self, game_data: GameData) -> bool:
        """Update player statistics based on bombs rule.
        :return: True if player's turn ends.

        .. note::
            **Rule**
            Life is reduced by 1 if player obtains three bombs.
        """
        player = game_data.current_player()
        counts = {i: player.dice_value.count(i) for i in player.dice_value}

        if "bomb" in counts.keys() and counts["bomb"] > 2:
            return self.visit_update_life(player, game_data, -1)

        return False

    def visit_update_life(
        self, player: Player, game_data: GameData, decrement: int = -1
    ) -> bool:
        """Updates life stat of current player by adding up the value specified.
        use a positive number to increment life and a negative number to perform
        a life decrement.

        :return: True if player's life reaches zero.
        """
        player.life += decrement

        if player.life <= 0:
            player.life = 0
            if game_data.is_first_death():
                player.status = Player.S_GHOST
            else:
                player.status = Player.S_DEAD
            return True

        return False

    def visit_arrows(self, game_data: GameData) -> bool:
        """Update player statistics based on arrows rule.
        :return: True if player's turn ends.

        .. note::
            **Rule**
            Life is reduced by the number of arrows the player has.
            If the arrows in the stack run out then the rule is
            applied to all the participants in the game.
        """
        player = game_data.current_player()
        counts = {i: player.dice_value.count(i) for i in player.dice_value}

        if "arrow" in counts.keys():
            if counts["arrow"] > game_data.arrows_left:
                player.arrows += game_data.arrows_left
                game_data.arrows_left = settings.MAX_ARROWS_COUNT
                for playr in game_data.player_list():
                    self.visit_update_life(playr, game_data, -playr.arrows)
                    playr.arrows = 0
                return True
            else:
                game_data.arrows_left -= counts["arrow"]
                player.arrows += counts["arrow"]

        return False

    def visit_shoot(self, game_data: GameData) -> bool:
        """Update player statistics based on shoot rule.
        :return: True if player's turn ends.

        .. note::
            **Rule**
            Life is reduced by 1 if player obtains a shoot.
        """
        player = game_data.current_player()
        counts = {i: player.dice_value.count(i) for i in player.dice_value}

        if "shoot" in counts.keys():
            return self.visit_update_life(player, game_data, -counts["shoot"])

        return False

    def visitHit(self, game_data: GameData, attack_vector) -> bool:
        """attack_vector(dictionary):
        1st element:
        - clockwise: Traverse players towards the right.
        - backwards: Traverse players towards the left.
        2nd element:
        - Integer list with how many shoots should be applied.

        e.g.:
        attack_vector = {
        'clockwise':[1,0,1], # Hit the first and third player on the right.
        'backwards':[0,2]    # Hit twice the second player on the left.

        }
        """
        player = game_data.current_player()
        playr = None

        for i in attack_vector["clockwise"]:
            playr = player.right_hand_player
            playr.life -= i

        for i in attack_vector["backwards"]:
            playr = player.left_hand_player
            playr.life -= i

        return False

    def visit_status(self, player: Player, game_data: GameData) -> bool:
        """Update player statistics based on status rule.
        :return: True if player's turn ends.

        .. note::
            **Rule**
            Player lost the game if his or her life goes to zero.
        """
        if player.life <= 0:
            if not game_data.is_first_death():
                player.status = Player.S_DEAD
                return True
            else:
                player.status = Player.S_GHOST

        return False

    def visit_finish_turn(self, game_data: GameData):
        """Update player statistics based on status rule.

        Performs teardown and wrapup actions on player data:
         - Reset dice status.
        """
        player = game_data.current_player()

        player.dice_value = ["", "", "", "", "", ""]
        player.dice_re_roll = [3, 3, 3, 3, 3, 3]
        game_data.next_player()
