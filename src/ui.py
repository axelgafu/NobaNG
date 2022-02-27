from typing import Tuple
import pygame
import state

# mypy, overloaded function.
from multipledispatch import dispatch  # type: ignore
from game_rules import GameData

from player import Player


pygame.init()
font = pygame.font.Font(None, 30)


#
# Class: UI
# ==============================================================================
class UI:
    def display(self, text):
        pass

    def inflate(self, state, player):
        pass


#
# Class: TextUI
# ==============================================================================
class TextUI(UI):
    def display(self, text):
        print(text)


#
# Class: GraphicalUI
# ==============================================================================
class GraphicalUI(UI):
    def __init__(self, surface: pygame.Surface) -> None:
        super().__init__()
        self.surface = surface

    # mypy, overloaded function.
    @dispatch(state.State, GameData)  # type: ignore
    def inflate(self, state: state.State, game_data: GameData):
        self.surface.fill("Black")

    # mypy, overloaded function.
    @dispatch(state.Quit, GameData)  # type: ignore
    def inflate(self, state: state.Quit, game_data: GameData):
        self.display("Quit - Thanks for playing NobaNG")

    # mypy, overloaded function.
    @dispatch(state.Lobby, GameData)  # type: ignore
    def inflate(self, state: state.Lobby, game_data: GameData):
        self.display(
            "Lobby - Waiting in lobby for players to join the\
             game (Down:add player; Right: continue)."
        )

    # mypy, overloaded function.
    @dispatch(state.GameStart, GameData)  # type: ignore
    def inflate(self, state: state.GameStart, game_data: GameData):
        self.display("GameStart - Starting game...")

    # mypy, overloaded function.
    @dispatch(state.PlayGame, GameData)  # type: ignore
    def inflate(self, state: state.PlayGame, game_data: GameData):
        player = game_data.current_player()

        self.display(
            f"PlayGame - {player.name}'s turn, {state.re_rol} remaining (press left to end turn)"
        )
        self.draw_status(game_data)

    # mypy, overloaded function.
    @dispatch(state.PerformActivity, GameData)  # type: ignore
    def inflate(self, state: state.PerformActivity, game_data: GameData):
        player = game_data.current_player()

        self.display("PerformActivity - Applying actions")
        if player is None:
            return
        self.draw_status(game_data)

    # mypy, overloaded function.
    @dispatch(state.GameOver, GameData)  # type: ignore
    def inflate(self, state: state.GameOver, game_data: GameData):
        self.display("Game Over")

    # mypy, overloaded function.
    @dispatch(state.Display, GameData)  # type: ignore
    def inflate(self, state: state.Display, game_data: GameData):
        self.display(state.get_message())

    def draw_status(self, game_data: GameData):
        player = game_data.current_player()
        w, _ = self.surface.get_size()

        self.draw_box(str(player.life), "image/lore/life.png", (10, 10))
        self.draw_box(str(player.arrows), "image/lore/arrow.png", (74, 10))
        self.draw_box(str(game_data.arrows_left),
                      "image/lore/arrow.png", (w - 64, 10))

    def sum_vectors(self, a: tuple, b: tuple) -> tuple:
        """Vector sum of the two tuples passed as parameter; both tuples/vectors
        should be of the same size.

        returns a tuple with the result.
        """
        return tuple(map(sum, zip(a, b)))

    def draw_box(
        self, text: str, image_path: str, coordinate: Tuple, size: Tuple = (64, 64)
    ):
        x, y = coordinate
        width, height = size
        local_font = pygame.font.Font(None, 50)
        box_area = pygame.Rect(x, y, width, height)

        text_surf = local_font.render(str(text), True, "Red")
        text_rect = text_surf.get_rect(
            topleft=self.sum_vectors(coordinate, (3, 3)))
        picture_surf = pygame.image.load(image_path).convert_alpha()
        picture_surf = pygame.transform.scale(
            picture_surf, self.sum_vectors(size, (-13, -13))
        )
        picture_rect = picture_surf.get_rect(
            center=self.sum_vectors(box_area.center, (6, 7))
        )

        pygame.draw.rect(self.surface, pygame.Color(64, 64, 128, 0), box_area)
        self.surface.blit(picture_surf, picture_rect)
        self.surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.surface, pygame.Color(
            128, 128, 128, 0), box_area, 2)

    def display(self, text: str, x: int = 10, y: int = 10):
        display_surface = pygame.display.get_surface()
        w, h = display_surface.get_size()
        x = w - 20
        y = h // 4 - 8
        debug_background = pygame.Rect(10, h // 4 * 3, x, y)

        pygame.draw.rect(display_surface, pygame.Color(
            64, 64, 64, 0), debug_background)
        debug_surf = font.render(text, True, "White")
        debug_rect = debug_surf.get_rect(topleft=(10 + 5, h // 4 * 3 + 5))
        pygame.draw.rect(display_surface, pygame.Color(
            64, 64, 64, 0), debug_rect)
        display_surface.blit(debug_surf, debug_rect)
        pygame.draw.rect(
            display_surface, pygame.Color(
                128, 128, 128, 0), debug_background, 3
        )
