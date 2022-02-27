from dataclasses import dataclass


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
        self.dice_re_roll = [3, 3, 3, 3, 3, 3]
        self.right_hand_player: Player = self
        self.left_hand_player: Player = self
        # mypy, Initializing to invalid value.
        self.character: Character = None  # type: ignore
        self.role = None


#
# Class: Character
# ==============================================================================
class Character:
    """Generic class to group all the characters in the game. This class will
    be used in python to find all the different characters in the game.
    """

    def __init__(self, name: str, description: str) -> None:
        """When a character is created it provides the necessary algorithms to
        update instances of the Player class but it also has the name and the
        description of the character.
        """
        self.name = name
        self.description = description

    def initialize(self, player: Player):
        """Generic implementation. It does nothing unless it is overwritten
        in the children classes.
        """
        pass

    def visit_character_stats_rules(self, player: Player):
        """Generic implementation. It does nothing unless it is overwritten
        in the children classes.
        """
        pass

    def visit_character_counter_rules(self, game_data, game_rules):
        """Generic implementation. It does nothing unless it is overwritten
        in the children classes.
        """
        pass


#
# Class: Elie
# ==============================================================================
class Elie(Character):
    """Moli Stark's card"""

    def __init__(self) -> None:
        super().__init__(
            "Moli Stark",
            "Cada vez que otro jugador deba perder 1 o más puntos de vida puedes perderlos en su lugar",
        )

    def initialize(self, player: Player):
        """Moly uses the following values for the game:

        +------+-------+
        | Stat | Value |
        +------+-------+
        | life |   8   |
        +------+-------+
        | Dice |   5   |
        +------+-------+
        """
        player.life = 8
        player.max_life = 8
        player.dice_count = 5


#
# Class: Bill
# ==============================================================================
class Bill(Character):
    """Bill Sin Rostro's card"""

    def __init__(self) -> None:
        super().__init__(
            "Bill Sin Rostro",
            "Aplica los resultados de flechas sólo después de tu última tirada.",
        )

    def initialize(self, player: Player):
        """Moly uses the following values for the game:

        +------+-------+
        | Stat | Value |
        +------+-------+
        | life |   9   |
        +------+-------+
        | Dice |   5   |
        +------+-------+
        """
        player.life = 9
        player.max_life = 9
        player.dice_count = 5


#
# Class: Doc
# ==============================================================================
class Doc(Character):
    """Doc Holiday's card"""

    def __init__(self) -> None:
        super().__init__(
            "Doc Holyday",
            "Cada vez que uses 3 o más disparos '1' y/o '2' tambièn recuperas 2 puntos de vida.",
        )

    def initialize(self, player: Player):
        """Moly uses the following values for the game:

        +------+-------+
        | Stat | Value |
        +------+-------+
        | life |   8   |
        +------+-------+
        | Dice |   5   |
        +------+-------+
        """
        player.life = 8
        player.max_life = 8
        player.dice_count = 5


#
# Class: Jose
# ==============================================================================
class Jose(Character):
    """Jose Delgado's card"""

    def __init__(self) -> None:
        super().__init__(
            "José Delgado",
            "Puedes usar el dado del Bocazas sin que sustituyan un dado básico (lanza 6 dados en total).",
        )

    def initialize(self, player: Player):
        """Moly uses the following values for the game:

        +------+-------+
        | Stat | Value |
        +------+-------+
        | life |   7   |
        +------+-------+
        | Dice |   6   |
        +------+-------+
        """
        player.life = 7
        player.max_life = 7
        player.dice_count = 6
