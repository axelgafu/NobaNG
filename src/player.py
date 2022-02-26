
from dataclasses import dataclass
        

    




#
# Class: Player 
#==============================================================================
@dataclass
class Player:
    """Data class that holds player's information.
    It is intended that this class only have variables (data). GameRules
    has the algorithms that updates player's data(visitor design pattern).
    """
    S_DEAD = 'dead'
    S_ALIVE = 'alive'
    S_GHOST = 'ghost'

    def __init__(self, name:str="") -> None:
        """When a player is created it will have unsuitable values for the
        game. Make sure to initialize them using the initialization visitors
        from GameRules"""
        self.name = name
        self.life = 0
        self.max_life = 0
        self.arrows = 0
        self.dice_count = 6
        self.status = Player.S_ALIVE
        self.dice_value = ['','','','','','']
        self.dice_re_roll = [3,3,3,3,3,3]
        self.right_hand_player:Player = self
        self.left_hand_player:Player = self
        self.character:Character = None # type: ignore # Initializing to invalid value.
        self.role = None
        

    




#
# Class: Character 
#==============================================================================
class Character:
    def __init__(self, name:str, description:str) -> None:
        self.name = name
        self.description = description
    
    def initialize(self, player: Player):
        pass

    def visit_character_stats_rules(self, player:Player):
        #print(f"Applying character stats rules {player.dice_value} - {player.status}")
        pass

    def visit_character_counter_rules(self, game_data, game_rules):
        #print("Applying character counter rules")
        pass
        

    




#
# Class: Elie 
#==============================================================================
class Elie(Character):
    def __init__(self) -> None:
        super().__init__(
            "Moli Stark",
            "Cada vez que otro jugador deba perder 1 o más puntos de vida puedes perderlos en su lugar")

    def initialize(self, player: Player):
        player.life = 8
        player.max_life = 8
        player.dice_count = 5
        

    




#
# Class: Bill 
#==============================================================================
class Bill(Character):
    def __init__(self) -> None:
        super().__init__(
            "Bill Sin Rostro",
            "Aplica los resultados de flechas sólo después de tu última tirada.")

    def initialize(self, player: Player):
        player.life = 8
        player.max_life = 8
        player.dice_count = 5
    

