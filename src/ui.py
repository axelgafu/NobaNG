from typing import Tuple
import pygame
import state

# mypy, overloaded function.
from multipledispatch import dispatch  # type: ignore
from game_rules import Die, GameData

from player import Player


pygame.init()
font = pygame.font.Font(None, 30)


#
# Class: UI
# ==============================================================================
class UI:
    """General class to handle game user interface. The resource where the user
    interface will be displayed should be controlled by the specific implementation
    of the class. Some examples of those user interface resources are (but not
    limitted to): a file, text on the screen, a database, the network or a
    graphical interface.
    """

    def display(self, text):
        """Overwrite this method to show a message in the output resource."""
        pass

    def inflate(self, state, player):
        """Overwrite this method to update the output resource based on game
        state and player data.
        """
        pass


#
# Class: TextUI
# ==============================================================================
class TextUI(UI):
    """This class implements a user interface based on text."""

    def display(self, text):
        """Use this method to output the message to the standard outoput (i.e.
        the screen).
        """
        print(text)


#
# Class: GraphicalUI
# ==============================================================================
class GraphicalUI(UI):
    """This class implements a user interface based on graphics."""

    def __init__(self, surface: pygame.Surface) -> None:
        super().__init__()
        self.surface = surface
        self.dice_selection = 0

    # mypy, overloaded function.
    @dispatch(state.State, GameData)  # type: ignore
    def inflate(self, state: state.State, game_data: GameData):
        """Base user interface update on a generic game state."""
        self.surface.fill("Black")

    # mypy, overloaded function.
    @dispatch(state.Quit, GameData)  # type: ignore
    def inflate(self, state: state.Quit, game_data: GameData):
        """Base user interface update on the "Quit" state.
        Graphical interface will show a thank you message before ending the game.
        """
        self.display("Quit - Thanks for playing NobaNG")

    # mypy, overloaded function.
    @dispatch(state.Lobby, GameData)  # type: ignore
    def inflate(self, state: state.Lobby, game_data: GameData):
        """Base user interface update on the "Lobby" state.
        The game directs the player on how to add users to the game round.
        """
        self.display(
            "Lobby - Waiting in lobby for players to join the\
             game (Down:add player; Right: continue)."
        )

    # mypy, overloaded function.
    @dispatch(state.GameStart, GameData)  # type: ignore
    def inflate(self, state: state.GameStart, game_data: GameData):
        """Base user interface update on the "GameStart" state.
        Game start is when the game players are assigned with a role and a
        character, so the GUI presents those data.

        Everybody can see each player character but at this point game
        players can only see their own role.
        """
        self.display("GameStart - Starting game...")

    # mypy, overloaded function.
    @dispatch(state.PlayGame, GameData)  # type: ignore
    def inflate(self, state: state.PlayGame, game_data: GameData):
        """Base user interface update on the "PlayGame" state.
        User stats are played and dice values for each player turn.
        """
        player = game_data.current_player()

        if state.sub_state == state.STATE_THROWING_DICE:
            self.display(
                f"PlayGame - {player.name}'s turn, {state.re_rol}\
                    remaining (press left to end turn)"
            )
        elif state.sub_state == state.STATE_PLAYER_DECIDING:
            self.visit_assign_dice(game_data.get_dice())

            if game_data.is_key_pressed(pygame.K_RIGHT):
                self.dice_selection += 1
                self.dice_selection = min(
                    self.dice_selection, player.dice_count - 1)
            elif game_data.is_key_pressed(pygame.K_LEFT):
                self.dice_selection -= 1
                self.dice_selection = max(self.dice_selection, 0)

        self.show_dice(player, self.dice_selection)
        self.draw_status(game_data)

    def visit_assign_dice(self, dice: list[Die]):
        print()
        pass

    # mypy, overloaded function.
    @dispatch(state.PerformActivity, GameData)  # type: ignore
    def inflate(self, state: state.PerformActivity, game_data: GameData):
        """Base user interface update on the "PerformActivity" state.
        Current player selections are made effective int this state but
        depending on other player's roles and characters someone could
        counterattack. All those animations should occur during this
        state.
        """
        player = game_data.current_player()

        self.display("PerformActivity - Applying actions")
        if player is None:
            return
        self.draw_status(game_data)

    # mypy, overloaded function.
    @dispatch(state.GameOver, GameData)  # type: ignore
    def inflate(self, state: state.GameOver, game_data: GameData):
        """Base user interface update on the "GameOver" state.
        Graphical interface only show the game over message while
        playing the animations of the other players.
        """
        self.display("Game Over")

    # mypy, overloaded function.
    @dispatch(state.Display, GameData)  # type: ignore
    def inflate(self, state: state.Display, game_data: GameData):
        """Base user interface update on the "Display" state.
        This state is intentended to show information to the player and
        the game can get here from any state. Graphical interface retrieves
        the message to display from the "Display" state object.
        """
        self.display(state.get_message())

    def draw_status(self, game_data: GameData):
        """Use this function to update the game status on the screen."""
        player = game_data.current_player()
        w, _ = self.surface.get_size()

        self.draw_box(str(player.life), "image/lore/life.png", (10, 10))
        self.draw_box(str(player.arrows), "image/lore/arrow.png", (74, 10))
        self.draw_box(str(game_data.arrows_left),
                      "image/lore/arrow.png", (w - 64, 10))

    def show_dice(self, player: Player, selection: int):
        display_surface = pygame.display.get_surface()
        w, h = display_surface.get_size()

        x_offset = w // 2 - player.dice_count * 64 // 2
        for i in range(0, player.dice_count):
            if player.dice_value[i] != "":
                self.draw_select_box(
                    i == selection,
                    f"image/lore/{player.dice_value[i]}.png",
                    (x_offset + 64 * i + 1, 10),
                )

    def sum_vectors(self, a: tuple, b: tuple) -> tuple:
        """Vector sum of the two tuples passed as parameter; both tuples/vectors
        should be of the same size.

        returns a tuple with the result.
        """
        return tuple(map(sum, zip(a, b)))

    def draw_select_box(
        self, selected: bool, image_path: str, coordinate: tuple, size: tuple = (64, 64)
    ):
        x, y = coordinate
        width, height = size
        local_font = pygame.font.Font(None, 50)
        box_area = pygame.Rect(x, y, width, height)

        picture_surf = pygame.image.load(image_path).convert_alpha()
        picture_surf = pygame.transform.scale(picture_surf, size)
        picture_rect = picture_surf.get_rect(center=box_area.center)

        pygame.draw.rect(self.surface, pygame.Color(64, 64, 128, 0), box_area)
        self.surface.blit(picture_surf, picture_rect)
        if selected:
            pygame.draw.rect(self.surface, pygame.Color(
                128, 0, 0, 0), box_area, 5)
        else:
            pygame.draw.rect(self.surface, pygame.Color(
                128, 128, 128, 0), box_area, 2)

    def draw_box(
        self, text: str, image_path: str, coordinate: tuple, size: tuple = (64, 64)
    ):
        """Use this function to show a square card with the text in the upper left
        corner and the image in the background.

        :param: text is a short message 2-3 characters length.
        :param: image_path is the place where the background image is.
        :param: coordinate is the location where the upper-left corner of the
            card should be drawn.
        :param: size is the dimention of the card (width, height),
            i.e. (64, 64) by default.
        """
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
        """Use this function to show a text in the area designated as
        output for the game.
        """
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
