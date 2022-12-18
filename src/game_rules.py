from dataclasses import dataclass
from random import randint

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

    It implements Singleton design pattern from `refactoring.guru <https://www.geeksforgeeks.org/singleton-pattern-in-python-a-complete-guide/>`_

    """

    _instance = None

    def __new__(self):
        """Implements singleton design pattern."""
        if self._instance is None:
            self._instance = super(GameData, self).__new__(
                self)  # (*args, **kwargs)

        return self._instance

    def __init__(self):
        """Initializes the data that is to be used during the Game.
        This class implements the singleton design pattern to keep consistency
        throughout the game.
        """
        self.keys = None
        self._prev_keys = None
        self._curr_keys = None
        self._player_list = {}
        self._player_head = None
        self._current_player = None
        self.arrows_left = settings.MAX_ARROWS_COUNT
        pygame.key.set_repeat(0)

    def player_list(self) -> list[Player]:
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
        self._prev_keys = self._curr_keys
        self._curr_keys = [k for k in keys]
        self.keys = keys

    def is_key_pressed(self, key: int) -> bool:
        """ "Use this method to test if the key pressed status has changed.
        :return: True if previous status is different and False otherwise.
        """
        key &= 0xFF
        return not self._prev_keys[key] and self._curr_keys[key]

    def is_key_released(self, key: int) -> bool:
        key &= 0xFF
        return self._prev_keys[key] and not self._curr_keys[key]

    def is_key_held(self, key: int) -> bool:
        key &= 0xFF
        return self._prev_keys[key] and self._curr_keys[key]

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

    def shuffle_dice(self, dice_playing: int = 100, brave: bool = False) -> list:
        rolling_player = self.current_player()
        self._dice = []

        for i in range(0, min(dice_playing, rolling_player.dice_count - 2)):
            self._dice.append(DieRegular(self).shuffle())

        if brave:
            self._dice.append(DieBrave(self).shuffle())
        else:
            self._dice.append(DieCoward(self).shuffle())

        return self._dice

    def get_dice(self) -> list:
        return self._dice

    def lock_dice(self, lock_value: str):
        [die.lock(lock_value) for die in self.get_dice()]


class GameRules:
    """This class is intended to hold all the algorithms that rule the game
    interactions with game players.
    It implements Singleton design pattern from `refactoring.guru <https://www.geeksforgeeks.org/singleton-pattern-in-python-a-complete-guide/>`_

    """

    _instance = None

    def __new__(self):
        """Implements singleton design pattern."""
        if self._instance is None:
            self._instance = super(GameRules, self).__new__(
                self)  # (*args, **kwargs)

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
        player.character = clazz(player)

    def visit_initialize_player(self, player: Player):
        """Applies the boosts and effects of the assigned character and role
        to the given player"""
        if player.character is not None:
            player.character.initialize()

    def visit_throw_dice(self, game_data: GameData, brave: bool) -> list:
        """Update player statistics based on dice rule.
        :return: False.

        .. note::
            **Rule**
            If player is alive, use `throw_alive`.
            If plaier is ghost, use `throw_ghost`.
        """
        result = []

        if game_data.current_player().status == Player.S_GHOST:
            result = self.throw_ghost(game_data)
        else:
            result = self.throw_alive(game_data, brave)

        self.visit_lock_dice(game_data)
        return result

    def throw_alive(self, game_data: GameData, brave) -> list:
        """Update player statistics based on alive dice rule.
        :return: True if player's turn ends.

        .. note::
            **Rule**
            Throw dice with full character capacity.
        """
        return game_data.shuffle_dice()

    def throw_ghost(self, game_data: GameData) -> list:
        """Update player statistics based on alive dice rule.
        :return: True if player's turn ends.

        .. note::
            **Rule**
            Throw just 2 dice.
        """
        return game_data.shuffle_dice(2)

    def visit_lock_dice(self, game_data: GameData) -> bool:
        """Use this method to update re-roll state of player's dice.
        :param player: Game player to be updated.
        :type player: Player
        :return: False
        """
        game_data.lock_dice("bomb")

        return False

    def visit_life(self, player: Player) -> bool:
        """Update player statistics based on life rule.
        :return: True if player's turn ends.

        .. note::
            **Rule**
            Whenever it is within the character limits:
            * If '2xlife' is obtained player gains two life points.
            * If 'life' is obtained player gains one life points.
        """
        counts = {i: player.dice_value.count(i) for i in player.dice_value}

        if "2xlife" in counts.keys():
            player.life += 2 * counts["2xlife"]

        if "life" in counts.keys():
            player.life += counts["life"]

        player.life = min(player.max_life, player.life)
        return False

    # def visit_character_stats_rules(self, player: Player) -> bool:
    #     player.character.visit_character_stats_rules(player)

    #     return False

    def visit_apply_dice_actions(self, game_data: GameData):
        for xdie in game_data.get_dice():
            die: Die = xdie
            die.execute()

    def visit_character_counter_rules(self, game_data: GameData) -> bool:
        player: Player = game_data.current_player()
        player.character.visit_character_counter_rules(game_data, self)

        return False

    def visit_hit(self, game_data: GameData, attack_vector: dict) -> bool:
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
        # player.dice_re_roll = [3, 3, 3, 3, 3, 3]
        game_data.next_player()


#
# Class: Die
# ==============================================================================


class Die:
    def __init__(self, game_data: GameData) -> None:
        self.value: str = ""
        self._target: Player
        self._game_data = game_data
        self._locked = False

    def get_dice(self) -> list[str]:
        return []

    def is_skippable(self) -> bool:
        return False

    def shuffle(self):
        """Use this method to "throw" the dice.
        :return Die: This Die.
        """
        if not self._locked:
            self.value = self.get_dice()[randint(0, 5)]
        return self

    def assign(self, target: Player) -> None:
        self._target = target

    def execute(self):
        """Implement this effect in concrete class."""
        self.visit_character_stats_rules()

    def get_available_targets(self, game_data: GameData) -> list[Player]:
        return self.identify_targets(game_data)

    def get_selected_targets(self) -> Player:
        return self._target

    def identify_targets(self, game_data: GameData) -> list[Player]:
        """Determines what players may be affected by this die."""
        rolling_player = game_data.current_player()

        if self.value in ["life", "no_arrow"]:
            return game_data.player_list()
        elif self.value in ["1", "2", "2x1", "2x2"]:
            result = []
            if rolling_player.character.visit_recognize_hit1(self.value):
                result.append(rolling_player.right_hand_player)
                result.append(rolling_player.left_hand_player)

            if rolling_player.character.visit_recognize_hit2(self.value):
                result.append(
                    rolling_player.right_hand_player.right_hand_player)
                result.append(rolling_player.left_hand_player.left_hand_player)

            return result
        elif self.value in ["bomb", "arrow", "shoot"]:
            return [rolling_player]
        else:
            raise RuntimeError(
                f"Unhandled die option {self.value}, implement handler.")

    def visit_arrows(self, decrement: int = -1) -> bool:
        """
        Update player statistics based on arrows rule.

        :param decrement: A negative number implies an arrow has been taken
            from the stack. A positive number means an arrow removal action
            was used.

        :type decrement: int
        :return: True if player's turn ends.

        .. note::
            **Rule**
            Life is reduced by the number of arrows the player has.
            If the arrows in the stack run out then the rule is
            applied to all the participants in the game.
        """
        self._game_data.arrows_left += decrement

        if self._game_data.arrows_left <= 0:
            self._target.arrows -= decrement
            self._game_data.arrows_left = settings.MAX_ARROWS_COUNT
            for player in self._game_data.player_list():
                self.visit_update_life(-player.arrows)
                player.arrows = 0
            return True
        else:
            self._game_data.arrows_left += decrement
            self._target.arrows -= decrement

        return False

    def visit_update_life(self, decrement: int = -1) -> bool:
        """Updates life stat of current player by adding up the value specified.
        use a positive number to increment life and a negative number to perform
        a life decrement.

        :return: True if player's life reaches zero.
        """
        self._target.life += decrement

        if self._target.life <= 0:
            self._target.life = 0
            if self._game_data.is_first_death():
                self._target.status = Player.S_GHOST
            else:
                self._target.status = Player.S_DEAD
            return True

        return False

    def lock(self, lock_value: str):
        self._locked = self.value == lock_value

    def visit_character_stats_rules(self):
        """."""
        self._target.character.visit_character_stats_rules(self.value)


class DieRegular(Die):
    def __init__(self, game_data: GameData) -> None:
        super().__init__(game_data)

    def get_dice(self) -> list[str]:
        return ["1", "2", "shoot", "arrow", "bomb", "life"]

    def execute(self):
        """Apply effects of Regular die."""
        if self.value in ["shoot", "1", "2"]:
            self.visit_update_life(-1)
        elif self.value in ["arrow"]:
            self.visit_arrows(-1)
        elif self.value in ["life"]:
            self.visit_update_life(+1)

        super().execute()


class DieBrave(Die):
    def __init__(self, game_data: GameData) -> None:
        super().__init__(game_data)

    def get_dice(self) -> list[str]:
        return ["2x1", "2x2", "bomb", "arrow", "shoot", "bullet"]

    def execute(self):
        """Apply effects of Brave die."""
        if self.value in ["2x1", "2x2"]:
            self.visit_update_life(-2)
        elif self.value in ["arrow"]:
            self.visit_arrows(-1)
        elif self.value in ["shoot", "bullet"]:
            self.visit_update_life(-1)


class DieCoward(Die):
    def __init__(self, game_data: GameData) -> None:
        super().__init__(game_data)

    def get_dice(self) -> list[str]:
        return ["1", "no_arrow", "bomb", "arrow", "2xlife", "life"]

    def execute(self):
        """Apply effects of Brave die."""
        if self.value in ["1"]:
            self.visit_update_life(-1)
        elif self.value in ["no_arrow"]:
            self.visit_arrows(+1)
        elif self.value in ["2xlife"]:
            self.visit_update_life(+2)
        elif self.value in ["life"]:
            self.visit_update_life(+1)
