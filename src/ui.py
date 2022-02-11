import pygame
pygame.init()
font = pygame.font.Font(None,30)

class TextUI:
    def display(self, text):
        print(text)
        self.debug(text)


    def debug(self,info,y = 10, x = 10):
        display_surface = pygame.display.get_surface()
        debug_surf = font.render(str(info),True,'White')
        debug_rect = debug_surf.get_rect(topleft = (x,y))
        pygame.draw.rect(display_surface,'Black',debug_rect)
        display_surface.blit(debug_surf,debug_rect)