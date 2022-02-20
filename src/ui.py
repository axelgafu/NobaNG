import pygame
import state

from multipledispatch import dispatch
from game_rules import GameData

from player import Player


pygame.init()
font = pygame.font.Font(None,30)


class UI:
    def display(self, text):
        pass

    def inflate(self, state, player):
       pass



class TextUI(UI):
    def display(self, text):
        print(text)



class GraphicalUI(UI):
    def __init__(self, surface:pygame.Surface) -> None:
        super().__init__()
        self.surface = surface



    @dispatch(state.State, GameData)
    def inflate(self, state:state.State, game_data:GameData):
       self.surface.fill('Black')



    @dispatch(state.Quit, GameData)
    def inflate(self, state:state.Quit, game_data:GameData):
        self.display('Thanks for playing NobaNG')



    @dispatch(state.Lobby, GameData)
    def inflate(self, state:state.Lobby, game_data:GameData):
        self.display("Waiting in lobby for players to join the game (Down:add player; Right: continue).")



    @dispatch(state.GameStart, GameData)
    def inflate(self, state:state.GameStart, game_data:GameData):
        self.display('Starting game...')



    @dispatch(state.PlayGame, GameData)
    def inflate(self, state:state.PlayGame, game_data:GameData):
        player = game_data.current_player()
        self.display(f"{player.name}'s turn, {state.re_rol} remaining (press left to end turn)")



    @dispatch(state.PerformActivity, GameData)
    def inflate(self, state:state.PerformActivity, game_data:GameData):
        player = game_data.current_player()

        self.display('Applying actions')
        if player is None:
            return
        self.draw_life(player)



    @dispatch(state.Display, GameData)
    def inflate(self, state:state.Display, game_data:GameData):
        self.display(state.get_message())


    def draw_life(self, player:Player):
        w, h = self.surface.get_size()
        box_area = pygame.Rect(10, h-64, 64, 64)

        pygame.draw.rect(self.surface, pygame.Color(128,64,64,0), box_area)
        local_font = pygame.font.Font(None,60)
        box_surf = local_font.render(str(player.life),True,'White')
        box_rect = box_surf.get_rect(topleft = (10, h-64))
        pygame.draw.rect(self.surface,pygame.Color(64,64,64,0),box_rect)
        self.surface.blit(box_surf,box_rect)
        pygame.draw.rect(self.surface,pygame.Color(128,128,128,0),box_area, 3)


    def display(self, text:str, x:int = 10, y:int = 10):
        display_surface = pygame.display.get_surface()
        w, h = display_surface.get_size()
        x = w-20
        y = h//3 - 8
        debug_background = pygame.Rect(10, h//3*2, x, y)

        pygame.draw.rect(display_surface, pygame.Color(64,64,64,0), debug_background)
        debug_surf = font.render(text,True,'White')
        debug_rect = debug_surf.get_rect(topleft = (10+5, h//3*2+5))
        pygame.draw.rect(display_surface,pygame.Color(64,64,64,0),debug_rect)
        display_surface.blit(debug_surf,debug_rect)
        pygame.draw.rect(display_surface, pygame.Color(128,128,128,0), debug_background, 3)