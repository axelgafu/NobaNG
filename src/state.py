import sys
from typing import Sequence
import pygame

#from ui import UI
from player import Player
from game_rules import GameRules, GameData





#
# Class: State 
#==============================================================================
class State:
    def __init__(self):
        self.state_id = 'ST_GENERAL'
        self._states_pool = {}
        self._transition_cooldown = 200
        self._transition_time = 0
        self._transitions_enabled = False
        
    def get_state(self, state_class_name) -> 'State':
        """Returns a `State`:class: object with current game state ready to
        execute next action.
        """
        if state_class_name not in self._states_pool.keys():
            current_module = sys.modules[__name__]
            klass = getattr(current_module, state_class_name)
            self._states_pool[state_class_name] = klass()

        return self._states_pool[state_class_name]

    
   
    def traverseState(self, game_data:GameData):
        """Performs current state actions, update players stats and 
        transitions to next state.
        """
        if game_data.keys is not None and self._transitions_enabled:
            self.set_transitionable(False)
            self.update(game_data)    
            transition = self.transitionate(game_data)
            if transition == None: # Implicitly return same state.
                #print(f"{self.__class__.__name__} -> {self.__class__.__name__}")
                return self
            else:
                #print(f"{self.__class__.__name__} -> {transition.__class__.__name__}")
                return transition
        
        #print(f"(Default) {self.__class__.__name__} -> {self.__class__.__name__}")
        return self

    def transitionate(self, game_data:GameData):
        pass

    def update(self, game_data:GameData):
        pass

    def set_transitionable(self, enabled:bool):
        self._transitions_enabled = enabled





#
# Class: Quit
#==============================================================================
class Quit(State):
    def __init__(self):
        super().__init__()
        self.state_id = 'ST_QUIT'
        self._updated = False

    def update(self, game_data):
        if not self._updated:
            self._updated = True





#
# Class: Lobby 
#==============================================================================
class Lobby(State):
    def __init__(self):
        super().__init__()        
        self.state_id = 'ST_LOBBY'


    def update(self, game_data:GameData):
        pass
        


    def transitionate(self, game_data):
        if game_data.keys[pygame.K_ESCAPE]:
            return self.get_state('Quit')

        if ((game_data.keys[pygame.K_RIGHT] and game_data.players_count() < 1) or
            game_data.keys[pygame.K_DOWN]):
            message, handler = self.handle_answer_add_user(game_data)
            return (self.get_state('Display')
                .message(message)
                .using(handler))
        else:
            return self.get_state('GameStart')

            
        
    def handle_answer_add_user(self, game_data:GameData):
        """High-order function, returns a message that should be shown to the
        player and the function that should be used to handle player's response
        to the displayed question.
        usage example:

        .. code-block:: python
            :emphasize-lines: 1,4,5

            message, handler = self.handle_answer_add_user(game_data)
            return (self.get_state('Display')
                .message(self,message)
                .using(handler))

        """
        message = f"Press Enter to add a default user: Player{game_data.players_count()+1}"
        def handle(display_state:Display, game_data:GameData) -> State:
            if game_data.keys[pygame.K_RETURN]:
                player = Player()
                player.name = f"Player{game_data.players_count()+1}"
                game_data.append_player(player)
            
            return self
        
        return message, handle




#
# Class: GameStart 
#==============================================================================
class GameStart(State):
    def __init__(self):
        super().__init__()        
        self.state_id = 'ST_GAME_START'
        self._updated = False
        self._game_rules = GameRules()


    def update(self, game_data:GameData):
        if not self._updated:
            for playr in game_data.player_list():
                self._game_rules.visitAssignCharacter(playr)
                self._game_rules.visitInitializePlayer(playr)
            self._updated = True


    def transitionate(self, game_data):
        self._updated = False
        if game_data.keys[pygame.K_RETURN]:
            return self.get_state('PlayGame')
        
        if game_data.keys[pygame.K_ESCAPE]:
            return self.get_state('Lobby')
        self._updated = True




#
# Class: PlayGame 
#==============================================================================
class PlayGame(State):
    def __init__(self):
        super().__init__()        
        self.state_id = 'ST_TURN'
        self.re_rol = 3
        self._game_rules = GameRules()


    def update(self, game_data:GameData):
        self.apply_rules(self._game_rules, game_data)



    def transitionate(self, game_data):
        if game_data.keys[pygame.K_ESCAPE]:
            return self.get_state('GameStart')

        if self.re_rol <= 0:
            # End of current player's turn
            self.re_rol = 3
            self._game_rules.visit_finish_turn(game_data)
            return self.get_state('PerformActivity')

        else:
            message, handler = self.handle_answer_rerol()
            return (self.get_state('Display')
                        .next_state(self)
                        .message(message)
                        .using(handler))
            
        
    def handle_answer_rerol(self):
        """High-order function, returns a message that should be shown to the
        player and the function that should be used to handle player's response
        to the displayed question.
        usage example:

        .. code-block:: python
            :emphasize-lines: 1,4,5

            message, handler = self.handle_answer_rerol()
            return (self.get_state('Display')
                .next_state(self)
                .message(message)
                .using(handler))

        """
        message = "Press up arrow to finish turn"
        def handle(display_state:Display, game_data:GameData) -> State:
            if game_data.keys[pygame.K_UP]:
                self.re_rol = 3
                self._game_rules.visit_finish_turn(game_data)
                return self.get_state('PerformActivity')

            elif game_data.keys[pygame.K_RETURN]:
                return self
            
            return display_state
        
        return message, handle
        


    def apply_rules(self, game_rules:GameRules, game_data:GameData):
        if self.re_rol <= 0:
            return # No more re-roles.

        player = game_data.current_player()
        end_player_turn = False

        game_rules.visit_throw_dice(player, brave=False)
        end_player_turn = (
            game_rules.visit_shoot(player) or
            game_rules.visit_bombs(player) or
            game_rules.visit_arrows(player, game_data.player_list) or
            game_rules.visit_status(player, game_data) or
            game_rules.visit_life(player) or
            game_rules.visit_character_stats_rules(player))

        if end_player_turn:
            self.re_rol = 0
        else:
            self.re_rol -= 1
        

    




#
# Class: PerformActivity 
#==============================================================================
class PerformActivity(State):
    def __init__(self):
        super().__init__()        
        self.state_id = 'ST_ACTIVITY'
        self._activity_performed = False
        self._game_rules = GameRules()


    def update(self, game_data:GameData):
        self._game_rules.visit_character_counter_rules(game_data)
        pass


    def transitionate(self, game_data):
        #
        # Automatic return on activity complete.
        #
        return self.get_state('PlayGame')
        

    




#
# Class: Display
#==============================================================================
class Display(State):
    def __init__(self):
        super().__init__()        
        self._activity_performed = False
        self._message = ""
        self._next_state = None
        self._display_time = 0
        self._display_duration = 2000

    def update(self, game_data):
        pass


    def message(self,message:str) -> 'State':
        self._message = message
        return self

    def next_state(self, next_state:State) -> 'State':
        self._next_state = next_state
        return self

    def get_message(self) -> str:
        return self._message


    def using(self, function) -> State:
        self._handler = function
        return self
        

    def transitionate(self, game_data:GameData):
        if self._handler is not None:
            next_state = self._handler(self, game_data)
            if next_state is not self:
                # Clean-up current state handler to avoid 
                # unwanted side effects.
                self._handler = None

            return next_state

        return self
 