import pygame, sys
from ui import *
from state import *
from settings import *

class Game:
    """
    .. image:: ../docsrc/image/diagram/state_diagram/StateMachine.png
    """
    def __init__(self):
          
        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
        pygame.display.set_caption('Noba BG')
        self.clock = pygame.time.Clock()
        self.state = Lobby()
        self.ui = GraphicalUI(self.screen)
        self.game_data = GameData()

    
    def run(self):
        self.screen.fill('black')
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or self.state.state_id == 'ST_QUIT':
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.game_data.update_keys(pygame.key.get_pressed())
                    self.state.set_transitionable(True)
                

            pygame.event.clear()
            self.state = self.state.traverseState(self.game_data)
            self.ui.inflate(self.state, self.game_data)
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()