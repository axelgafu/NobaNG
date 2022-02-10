import sys
import pygame

class GameData:
    def __init__(self):
        self.keys = None
        pygame.key.set_repeat(0)

    def update_keys(self):
        self.keys = pygame.key.get_pressed()

class State:
    def __init__(self, ui):
        self.state_id = 'ST_GENERAL'
        self._states_pool = {}
        self._transition_cooldown = 200
        self._transition_time = 0
        self._ui = ui
        self._transitions_enabled = True
        
    def get_state(self, state_class_name):
        if state_class_name not in self._states_pool.keys():
            current_module = sys.modules[__name__]
            klass = getattr(current_module, state_class_name)
            self._states_pool[state_class_name] = klass(self._ui)

        return self._states_pool[state_class_name]
   
    def traverseState(self, game_data):
        game_data.update_keys()

        if self._transitions_enabled:
            self._transitions_enabled = False
            self.update(game_data)

            if game_data.keys != None:
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

    def update(self, game_data):
        self._ui.display('Thanks for playing NobaNG')


class Turn(State):
    def __init__(self, ui):
        super().__init__(ui)        
        self.state_id = 'ST_TURN'
        self._played = False


    def update(self, game_data):
        if not self._played:
            self._ui.display('Playing turn')
            self._played = True


    def transitionate(self, game_data):
        if game_data.keys[pygame.K_ESCAPE]:
            return self.get_state('Quit')

        elif game_data.keys[pygame.K_RIGHT]:
            self._played = False
            return self.get_state('Activity')


class Activity(State):
    def __init__(self, ui):
        super().__init__(ui)        
        self.state_id = 'ST_ACTIVITY'


    def update(self, game_data):
        self._ui.display('Applying actions')


    def transitionate(self, game_data):
        if game_data.keys[pygame.K_RETURN]:
            return self.get_state('Turn')