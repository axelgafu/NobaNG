import sys
import pygame

from player import Player, GameRules

class GameData:
    def __init__(self):
        self.keys = None
        self._player_list = {}
        self._player_head = None
        self._current_player = None
        pygame.key.set_repeat(0)

    def player_list(self) -> 'list':
        return list(self._player_list.values())

    def next_player(self):
        if self._current_player is not None:
            self._current_player = self._current_player.right_hand_player
        else:
            self._current_player = self._player_head

    def current_player(self) -> 'Player':
        if self._current_player is None:
            self._current_player = self._player_head

        return self._current_player

    def update_keys(self):
        self.keys = pygame.key.get_pressed()

    def add_player(self, player):
        if player.name not in self._player_list.keys():
            if self._player_head is not None:
                player.left_hand_player = self._player_head
                
                player.right_hand_player = self._player_head.right_hand_player
                self._player_head.right_hand_player = player

            self._player_list[player.name] = player
            self._player_head = player

class State:
    def __init__(self, ui):
        self.state_id = 'ST_GENERAL'
        self._states_pool = {}
        self._transition_cooldown = 200
        self._transition_time = 0
        self._ui = ui
        self._transitions_enabled = False
        
    def get_state(self, state_class_name) -> 'State':
        if state_class_name not in self._states_pool.keys():
            current_module = sys.modules[__name__]
            klass = getattr(current_module, state_class_name)
            self._states_pool[state_class_name] = klass(self._ui)

        return self._states_pool[state_class_name]
   
    def traverseState(self, game_data):
        game_data.update_keys()
        self.update(game_data)
        if game_data.keys != None and self._transitions_enabled:
            transition = self.transitionate(game_data)
            if transition == None: # Implicitly return same state.
                return self
            else:
                return transition
            
        return self

    def transitionate(self, game_data):
        pass

    def update(self, game_data):
        pass

    def set_transitionable(self, enabled):
        self._transitions_enabled = enabled

class Quit(State):
    def __init__(self, ui):
        super().__init__(ui)
        self.state_id = 'ST_QUIT'
        self._updated = False

    def update(self, game_data):
        if not self._updated:
            self._ui.display('Thanks for playing NobaNG')
            self._updated = True

class Lobby(State):
    def __init__(self, ui):
        super().__init__(ui)        
        self.state_id = 'ST_LOBBY'
        self._updated = False


    def update(self, game_data):
        if not self._updated:
            self._ui.display('Waiting in Lobby')
            self._updated = True
        
        if game_data.keys[pygame.K_RETURN]:
            player = Player()
            self._ui.display("Player name: ")
            player.name = input()
            game_data.add_player(player)


    def transitionate(self, game_data):
        self._updated = False
        if game_data.keys[pygame.K_RIGHT]:
            return self.get_state('GameStart')

        if game_data.keys[pygame.K_ESCAPE]:
            return self.get_state('Quit')
        self._updated = True

class GameStart(State):
    def __init__(self, ui):
        super().__init__(ui)        
        self.state_id = 'ST_GAME_START'
        self._updated = False
        self._game_rules = GameRules()


    def update(self, game_data:GameData):
        if not self._updated:
            self._ui.display('Starting game...')
            for playr in game_data.player_list():
                self._game_rules.visitAssignCharacter(playr)
                self._game_rules.visitInitializePlayer(playr)
                self.summary(playr)
            self._updated = True

    def summary(self, player:Player):
        self._ui.display(
            f"""Name: {player.name}/{player.character.name}, Life:{player.life}, Dice:{player.dice_count}
            {player.dice_value}""")

    def transitionate(self, game_data):
        self._updated = False
        if game_data.keys[pygame.K_RETURN]:
            return self.get_state('Turn')
        
        if game_data.keys[pygame.K_ESCAPE]:
            return self.get_state('Lobby')
        self._updated = True

class Turn(State):
    def __init__(self, ui):
        super().__init__(ui)        
        self.state_id = 'ST_TURN'
        self._played = False
        self._game_rules = GameRules()


    def update(self, game_data:GameData):
        if not self._played:
            game_data.next_player()
            self._ui.display(f'Playing turn {game_data.current_player().name} (Esc:Exit, ->:Apply)')
            die_re_roll = [True,True,True,True,True,True]
            self._game_rules.visitThrowDice(game_data.current_player(), die_re_roll, brave=False)
            print(game_data.current_player().dice_value)
            self._played = True


    def transitionate(self, game_data):
        if game_data.keys[pygame.K_ESCAPE]:
            return self.get_state('GameStart')

        elif game_data.keys[pygame.K_RIGHT]:
            self._played = False
            return self.get_state('Activity')

class Activity(State):
    def __init__(self, ui):
        super().__init__(ui)        
        self.state_id = 'ST_ACTIVITY'
        self._activity_performed = False


    def update(self, game_data):
        if not self._activity_performed:
            self._activity_performed = True
            self._ui.display('Applying actions')


    def transitionate(self, game_data):
        if game_data.keys[pygame.K_RETURN]:
            self._activity_performed = False
            return self.get_state('Turn')