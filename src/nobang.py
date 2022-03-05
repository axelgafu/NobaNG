import pygame
import sys
from ui import *
from state import *
from settings import *


class Game:
    """The following state diagram shows the behavior of the game screens:

    .. image:: image/diagram/state_diagram/StateMachine.png

    .. image:: image/docstr-cov.svg

    Report of unit testing generated with pynguin cab be seen in the following
    link `Test Report <_static/test_report.html>`_

    """

    def __init__(self):
        """Initialize overal game."""

        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption("Noba BG")
        self.clock = pygame.time.Clock()
        self.state = Lobby()
        self.ui = GraphicalUI(self.screen)
        self.game_data = GameData()

    def run(self):
        """Big-Loop where the games resides in."""
        self.screen.fill("black")
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or self.state.state_id == "ST_QUIT":
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


if __name__ == "__main__":
    game = Game()
    game.run()
