import string


class Player:
    def __init__(self, name:string="") -> None:
        self.name = name
        self.life = 0
        self.arrows = 0
        self.dice_count = 6
        self.status = 'alive'
        self.dice_value = ['','','','','','']
        self.dice_re_roll = [3,3,3,3,3,3]
        self.right_hand_player = self
        self.left_hand_player = self
        self.character = None
        self.role = None

class Character:
    def __init__(self, name:str, description:str) -> None:
        self.name = name
        self.description = description
    
    def initialize(self):
        pass

    def visit_character_stats_rules(self, player):
        print("Applying character stats rules")
        pass

    def visit_character_counter_rules(self, game_data, game_rules):
        print("Applying character counter rules")
        pass
        

class Elie(Character):
    def __init__(self) -> None:
        super().__init__(
            "Moli Stark",
            "Cada vez que otro jugador deba perder 1 o más puntos de vida puedes perderlos en su lugar")

    def initialize(self, player: Player):
        player.life = 8
        player.dice_count = 5
        

class Bill(Character):
    def __init__(self) -> None:
        super().__init__(
            "Bill Sin Rostro",
            "Aplica los resultados de flechas sólo después de tu última tirada.")

    def initialize(self, player: Player):
        player.life = 8
        player.dice_count = 5
    

