import string
import settings

from random import seed, randint
from collections import Counter


seed(2022-2-10)

class Player:
    def __init__(self, name:string="") -> None:
        self.name = name
        self.life = 0
        self.arrows = 0
        self.dice_count = 6
        self.dice_value = ['','','','','','']
        self.right_hand_player = self
        self.left_hand_player = self
        self.character = None
        self.role = None

class Character:
    def __init__(self, name:str) -> None:
        self.name = name
    
    def initialize(self):
        pass
        

class Elie(Character):
    def __init__(self) -> None:
        super().__init__('Elie')

    def initialize(self, player: Player):
        player.life = 8
        player.dice_count = 5
    

class GameRules:
    def __init__(self) -> None:
        self._dice_list = {
            'regular':['1','2','shoot','arrow','bomb','life'],
            'brave':['2x1','2x2', 'bomb','arrow','shoot','bullet'],
            'coward':['1','no_arrow', 'bomb','arrow','2xlife','life'],
        }
        self.arrows_left = settings.MAX_ARROWS_COUNT

    def visitAssignCharacter(self, player:Player):
        player.character = Elie()

    def visitInitializePlayer(self, player:Player):
        if player.character is not None:
            player.character.initialize(player)

    def visitThrowDice(self, player, die_re_roll, brave:bool):
        if die_re_roll[0]:
            if brave:
                player.dice_value[0] = self._dice_list['brave'][randint(0,5)]
            else:
                player.dice_value[0] = self._dice_list['coward'][randint(0,5)]

        for i in range(1,player.dice_count):
            if die_re_roll[i]:
                player.dice_value[i] = self._dice_list['regular'][randint(0,5)]
                die_re_roll[i] = player.dice_value[i] != 'bomb'


    def visitLife(self, player:Player) -> 'bool':
        counts = dict(player.dice_value)
        player.life += 2*counts['2xLife'] + counts['Life']
        return False            
    
    def visitBombs(self, player:Player) -> 'bool':
        counts = dict(player.dice_value)
        if counts['bomb'] > 2:
            player.life -= 1
            return True
        
        return False

    def visitArrows(self, player:Player, player_list) -> 'bool':
        counts = dict(player.dice_value)
         
        if counts['arrow'] > self.arrows_left:
            player.arrows += self.arrows_left
            self.arrows_left = settings.MAX_ARROWS_COUNT
            for playr in player_list:                
                playr.life -= playr.arrows
                playr.arrows = 0
            return True
        else:
            self.arrows_left -= counts['arrow']
            player.arrows += counts['arrow']
        
        return False

    def visitShoot(self, player:Player) -> 'bool':
        counts = dict(player.dice_value)
        player.life -= counts['shoot']
        return False


    def visitHit(self, player:Player, attack_vector) -> 'bool':
        """
        attack_vector(dictionary):
            1st element:
             - clockwise: Traverse players towards the right.
             - backwards: Traverse players towards the left.
            2nd element:
             - Integer list with how many shoots should be applied.
        
        e.g.:
        attack_vector = {
            'clockwise':[1,0,1], # Hit the first and third player on the right.
            'backwards':[0,2], # Hit twice the second player on the left.
            }
        """
        playr = None

        for i in attack_vector['clockwise']:
            playr = player.right_hand_player    
            playr.life -= i
        
        for i in attack_vector['backwards']:
            playr = player.left_hand_player    
            playr.life -= i

        return False            

    def visitStatus(self, player:Player) -> 'bool':
        if player.life <= 0:
            player.status = 'dead'
            return True
        
        return False
