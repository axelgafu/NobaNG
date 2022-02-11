import pygame, sys
from ui import *
from state import *
from settings import *

class Game:
    def __init__(self):
          
        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
        pygame.display.set_caption('Noba BG')
        self.clock = pygame.time.Clock()
        self.state = Lobby(TextUI())
        self.game_data = GameData()

    
    def run(self):
        self.screen.fill('black')
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or self.state.state_id == 'ST_QUIT':
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.state.set_transitionable(True)

            self.state = self.state.traverseState(self.game_data)
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()