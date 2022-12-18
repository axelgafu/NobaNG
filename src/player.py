from dataclasses import dataclass
from math import fabs


#
# Class: Player
# ==============================================================================
@dataclass
class Player:
    """Data class that holds player's information.
    It is intended that this class only have variables (data). GameRules
    has the algorithms that updates player's data(visitor design pattern).
    """

    S_DEAD = "dead"
    S_ALIVE = "alive"
    S_GHOST = "ghost"

    def __init__(self, name: str = "") -> None:
        """When a player is created it will have unsuitable values for the
        game. Make sure to initialize them using the initialization visitors
        from GameRules"""
        self.name = name
        self.life = 0
        self.max_life = 0
        self.arrows = 0
        self.dice_count = 6
        self.status = Player.S_ALIVE
        self.dice_value = ["", "", "", "", "", ""]
        # self.dice_re_roll = [3, 3, 3, 3, 3, 3]
        self.right_hand_player: Player = self
        self.left_hand_player: Player = self
        # mypy, Initializing to invalid value.
        self.character: Character = None  # type: ignore
        self.role = None

        #
        # e.g.:
        #    attack_vector = {
        #        'clockwise':[1,0,1], # Hit the first and third player on the right.
        #        'backwards':[0,2]    # Hit twice the second player on the left.
        #    }
        self.attack_vector: dict = {
            "clockwise": [],
            "backwards": [],
        }


#
# Class: Character
# ==============================================================================
class Character:
    """Generic class to group all the characters in the game. This class will
    be used in python to find all the different characters in the game.
    """

    def __init__(self, player: Player, name: str, description: str) -> None:
        """When a character is created it provides the necessary algorithms to
        update instances of the Player class but it also has the name and the
        description of the character.
        """
        self.name = name
        self.description = description
        self.player: Player = player

    def initialize(self):
        """Generic implementation. It does nothing unless it is overwritten
        in the children classes.
        """
        pass

    def visit_character_stats_rules(self, die_value: str):
        """Generic implementation. It does nothing unless it is overwritten
        in the children classes.
        """
        pass

    def visit_character_counter_rules(self, game_data, game_rules):
        """Generic implementation. It does nothing unless it is overwritten
        in the children classes.
        """
        pass

    def visit_recognize_hit1(self, die_value: str) -> bool:
        return die_value == "1" or die_value == "2x1"

    def visit_recognize_hit2(self, die_value: str) -> bool:
        return die_value == "2" or die_value == "2x2"


#
# Class: Elie
# ==============================================================================
class Elie(Character):
    """Moli Stark's card"""

    def __init__(self, player: Player) -> None:
        super().__init__(
            player,
            "Moli Stark",
            "Cada vez que otro jugador deba perder 1 o más puntos de vida puedes perderlos en su lugar",
        )

    def initialize(self):
        """Moly uses the following values for the game:

        +------+-------+
        | Stat | Value |
        +------+-------+
        | life |   8   |
        +------+-------+
        | Dice |   5   |
        +------+-------+
        """
        self.player.life = 8
        self.player.max_life = 8
        self.player.dice_count = 5

    def visit_character_counter_rules(self, game_data, game_rules):
        """Whenever another player has to loose 1 or more life points, this
        character can loose them instead.

        :param game_data: Overall game data.
        :type game_data: GameData
        :param game_rules: Rules to be used in the game.
        :type game_rules: GameRules
        """
        curr_player = game_data.current_player()
        for die in game_data.get_dice():
            if die.value in ["1", "2"]:
                die.assign(self.player)

        # target player = {curr player targets}
        # character player chooses single target.
        pass


#
# Class: Bill
# ==============================================================================
class Bill(Character):
    """Bill Sin Rostro's card"""

    def __init__(self, player: Player) -> None:
        super().__init__(
            player,
            "Bill Sin Rostro",
            "Aplica los resultados de flechas sólo después de tu última tirada.",
        )

    def initialize(self):
        """Moly uses the following values for the game:

        +------+-------+
        | Stat | Value |
        +------+-------+
        | life |   9   |
        +------+-------+
        | Dice |   5   |
        +------+-------+
        """
        self.player.life = 9
        self.player.max_life = 9
        self.player.dice_count = 5


#
# Class: Doc
# ==============================================================================
class Doc(Character):
    """Doc Holiday's card"""

    def __init__(self, player: Player) -> None:
        super().__init__(
            player,
            "Doc Holyday",
            "Cada vez que uses 3 o más disparos '1' y/o '2' también recuperas 2 puntos de vida.",
        )

    def initialize(self):
        """Moly uses the following values for the game:

        +------+-------+
        | Stat | Value |
        +------+-------+
        | life |   8   |
        +------+-------+
        | Dice |   5   |
        +------+-------+
        """
        self.player.life = 8
        self.player.max_life = 8
        self.player.dice_count = 5

    def visit_character_stats_rules(self, die_value: str):
        """When dice have 3 or more hits labeled as "1" or "2", player recovers
        2 life points.
        """
        if die_value in ["1", "2"]:
            self.player.life = self.player.life + 2


#
# Class: Jose
# ==============================================================================
class Jose(Character):
    """Jose Delgado's card"""

    def __init__(self, player: Player) -> None:
        super().__init__(
            player,
            "José Delgado",
            "Puedes usar el dado del Bocazas sin que sustituyan un dado básico (lanza 6 dados en total).",
        )

    def initialize(self):
        """Moly uses the following values for the game:

        +------+-------+
        | Stat | Value |
        +------+-------+
        | life |   7   |
        +------+-------+
        | Dice |   6   |
        +------+-------+
        """
        self.player.life = 7
        self.player.max_life = 7
        self.player.dice_count = 6
