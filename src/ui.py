from typing import Tuple
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
        self.display('Quit - Thanks for playing NobaNG')



    @dispatch(state.Lobby, GameData)
    def inflate(self, state:state.Lobby, game_data:GameData):
        self.display("Lobby - Waiting in lobby for players to join the game (Down:add player; Right: continue).")



    @dispatch(state.GameStart, GameData)
    def inflate(self, state:state.GameStart, game_data:GameData):
        self.display('GameStart - Starting game...')



    @dispatch(state.PlayGame, GameData)
    def inflate(self, state:state.PlayGame, game_data:GameData):
        player = game_data.current_player()
        
        self.display(f"PlayGame - {player.name}'s turn, {state.re_rol} remaining (press left to end turn)")
        self.draw_status(game_data)



    @dispatch(state.PerformActivity, GameData)
    def inflate(self, state:state.PerformActivity, game_data:GameData):
        player = game_data.current_player()
        
        self.display('PerformActivity - Applying actions')
        if player is None:
            return
        self.draw_status(game_data)


    @dispatch(state.GameOver, GameData)
    def inflate(self, state:state.GameOver, game_data:GameData):
        self.display("Game Over")


    @dispatch(state.Display, GameData)
    def inflate(self, state:state.Display, game_data:GameData):
        self.display(state.get_message())



    def draw_status(self, game_data:GameData):
        player = game_data.current_player()
        w, _ = self.surface.get_size()

        self.draw_box(player.life, 'image/lore/life.png', (10,10))        
        self.draw_box(player.arrows, 'image/lore/arrow.png', (74,10))
        self.draw_box(game_data.arrows_left, 'image/lore/arrow.png', (w-64,10))


    def draw_box(self, text:str, image_path:str, coordinate:Tuple, size:Tuple=(64,64)):
        x,y = coordinate
        width,height = size
        local_font = pygame.font.Font(None,50)
        box_area = pygame.Rect(x, y, width, height)

        text_surf = local_font.render(str(text),True,'Red')
        text_rect = text_surf.get_rect(topleft = coordinate + pygame.Vector2((3,3)))
        picture_surf = pygame.image.load(image_path).convert_alpha()
        picture_surf = pygame.transform.scale(picture_surf, size - pygame.Vector2((13,13)))
        picture_rect = picture_surf.get_rect(center = box_area.center + pygame.Vector2((6,7)))

        pygame.draw.rect(self.surface,pygame.Color(64,64,128,0),box_area)
        self.surface.blit(picture_surf,picture_rect)
        self.surface.blit(text_surf,text_rect)
        pygame.draw.rect(self.surface,pygame.Color(128,128,128,0),box_area, 2)



    def display(self, text:str, x:int = 10, y:int = 10):
        display_surface = pygame.display.get_surface()
        w, h = display_surface.get_size()
        x = w-20
        y = h//4 - 8
        debug_background = pygame.Rect(10, h//4*3, x, y)

        pygame.draw.rect(display_surface, pygame.Color(64,64,64,0), debug_background)
        debug_surf = font.render(text,True,'White')
        debug_rect = debug_surf.get_rect(topleft = (10+5, h//4*3+5))
        pygame.draw.rect(display_surface,pygame.Color(64,64,64,0),debug_rect)
        display_surface.blit(debug_surf,debug_rect)
        pygame.draw.rect(display_surface, pygame.Color(128,128,128,0), debug_background, 3)