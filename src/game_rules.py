from typing import Sequence
import settings
import pygame

from player import Player, Elie
from random import seed, randint

seed(2022-2-10)
#
# Class: GameData 
#==============================================================================
class GameData:
    """Holds game state meta-data.

    This class represents the overall game moderator and it is updated by the 
    game states.
    """

    def __init__(self):
        self.keys = None
        self._player_list = {}
        self._player_head = None
        self._current_player = None
        pygame.key.set_repeat(0)



    def player_list(self) -> 'list':
        """Returns a `list` of `Player` objects where each element represents
        one of the players in the game.
        """
        return list(self._player_list.values())



    def next_player(self) -> 'Player':
        """Returns a `Player` object with the information of the **next** player.
        Calling this function moves game state to the next player.
        """
        if self._current_player is not None:
            self._current_player = self._current_player.right_hand_player
        else:
            self._current_player = self._player_head



    def current_player(self) -> 'Player':
        """Returns a `Player` object with the information of **current** player.
        Calling this function does not change game state.
        """
        if self._current_player is None:
            self._current_player = self._player_head

        return self._current_player



    def update_keys(self, keys:Sequence):
        """Use this function to read user input.
        User input is read from keyboard and it is read one key at a time. Each
        input is processed against the game state. Depending on the input, game
        state may change or not.

        For more information about how user input may change game state, please
        refer to the specific game states (`State` class)
        """
        self.keys = keys



    def append_player(self, player:Player):
        """Adds a new player to the game room.
        """
        if player.name not in self._player_list.keys():
            if self._player_head is not None:
                player.left_hand_player = self._player_head
                
                player.right_hand_player = self._player_head.right_hand_player
                self._player_head.right_hand_player = player

            self._player_list[player.name] = player
            self._player_head = player



    def players_count(self) -> 'int':
        """Returns an `int` that represents how many players are in the game.
        """
        return len(self._player_list)



class GameRules:
    _instance = None

    def __call__(self, *args, **kwargs):
        """Implements Singleton design pattern from
        `refactoring.guru <https://refactoring.guru/es/design-patterns/singleton/python/example>`
        """
        if self._instance is None:
            self._instance = super().__call__(*args, **kwargs)

        return self._instance


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

    def visit_throw_dice(self, player:Player, brave:bool) -> 'bool':
        """Update player statistics based on dice rule.
        :return: True if player's turn ends.

        .. note::
            **Rule**
            If player is alive, use `throw_alive`.
            If plaier is ghost, use `throw_ghost`.
        """
        if player.status == 'ghost':
            self.throw_ghost(player)
        else:
            self.throw_alive(player, brave)

        return False



    def throw_alive(self, player:Player, brave):
        """Update player statistics based on alive dice rule.
        :return: True if player's turn ends.

        .. note::
            **Rule**
            Throw dice with full character capacity.
        """
        if player.dice_re_roll[0]>0:
            if brave:
                player.dice_value[0] = self._dice_list['brave'][randint(0,5)]
            else:
                player.dice_value[0] = self._dice_list['coward'][randint(0,5)]
            player.dice_re_roll[0] -= 1

        for i in range(1,player.dice_count):
            if player.dice_re_roll[i]>0:
                player.dice_re_roll[0] -= 1
                player.dice_value[i] = self._dice_list['regular'][randint(0,5)]
                if(player.dice_value[i] == 'bomb'):
                    player.dice_re_roll[i] = 0



    def throw_ghost(self, player:Player):
        """Update player statistics based on alive dice rule.
        :return: True if player's turn ends.

        .. note::
            **Rule**
            Throw just 2 dice.
        """
        for i in range(0,1):
            if player.dice_re_roll[i]>0:
                player.dice_re_roll[0] -= 1
                player.dice_value[i] = self._dice_list['regular'][randint(0,5)]
                if(player.dice_value[i] == 'bomb'):
                    player.dice_re_roll[i] = 0



    def visit_life(self, player:Player) -> 'bool':
        counts = {i:player.dice_value.count(i) for i in player.dice_value}

        if '2xlife' in counts.keys():
            player.life += 2*counts['2xlife']
        
        if 'life' in counts.keys():
            player.life += counts['life']

        return False



    def visit_character_stats_rules(self, player:Player) -> 'bool':
        player.character.visit_character_stats_rules(player)

        return False



    def visit_character_counter_rules(self, game_data:GameData) -> 'bool':
        game_data.current_player().character.visit_character_counter_rules(game_data, self)

        return False


    
    def visit_bombs(self, player:Player) -> 'bool':
        """Update player statistics based on bombs rule.
        :return: True if player's turn ends.

        .. note::
            **Rule**
            Life is reduced by 1 if player obtains three bombs.
        """
        counts = {i:player.dice_value.count(i) for i in player.dice_value}
        
        if 'bomb' in counts.keys() and counts['bomb'] > 2:
            player.life -= 1
            return True
        
        return False



    def visit_arrows(self, player:Player, player_list) -> 'bool':
        """Update player statistics based on arrows rule.
        :return: True if player's turn ends.

        .. note::
            **Rule**
            Life is reduced by the number of arrows the player has.
            If the arrows in the stack run out then the rule is 
            applied to all the participants in the game.
        """
        counts = {i:player.dice_value.count(i) for i in player.dice_value}
        
        if 'arrow' in counts.keys():
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



    def visit_shoot(self, player:Player) -> 'bool':
        """Update player statistics based on shoot rule.
        :return: True if player's turn ends.

        .. note::
            **Rule**
            Life is reduced by 1 if player obtains a shoot.
        """
        counts = {i:player.dice_value.count(i) for i in player.dice_value}
        
        if 'shoot' in counts.keys():
            player.life -= counts['shoot']
        
        return player.life < 1
        



    def visitHit(self, player:Player, attack_vector) -> 'bool':
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
        playr = None

        for i in attack_vector['clockwise']:
            playr = player.right_hand_player    
            playr.life -= i
        
        for i in attack_vector['backwards']:
            playr = player.left_hand_player    
            playr.life -= i

        return False            



    def visit_status(self, player:Player, game_data:GameData) -> 'bool':
        """Update player statistics based on status rule.
        :return: True if player's turn ends.

        .. note::
            **Rule**
            Player lost the game if his or her life goes to zero.
        """
        if player.life <= 0:
            if not game_data.is_first_death():
                player.status = 'dead'
                return True
            else:
                player.status = 'ghost'
        
        return False            



    def visit_finish_turn(self, game_data:GameData):
        """Update player statistics based on status rule.

        Performs teardown and wrapup actions on player data:
         - Reset dice status.
        """
        player = game_data.current_player()

        player.dice_value = ['','','','','','']
        player.dice_re_roll = [3,3,3,3,3,3]
        game_data.next_player()
