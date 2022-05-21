import pygame
from settings import *

class DieScreen():
    def __init__(self,player):
        self.display_surface = pygame.display.get_surface()
        self.player = player

        self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE * 3)
        self.fontExp = pygame.font.Font(UI_FONT, UI_FONT_SIZE * 2)

        self.font_surface = self.font.render('YOU DIED',False,TEXT_COLOR)
        self.font_rect = self.font_surface.get_rect(midtop = (self.display_surface.get_size()[0] * 0.5,self.display_surface.get_size()[1] * 0.1))

        self.font_Expsurface = self.fontExp.render(f'SCORE:{int(self.player.exp)}', False, TEXT_COLOR)
        self.font_Exprect = self.font_Expsurface.get_rect(midtop = (WIDTH * 0.5, HEIGHT * 0.66))

        self.rect = pygame.Rect(WIDTH * 0.3,HEIGHT * 0.1, 500,70)
        self.Exprect = pygame.Rect(WIDTH * 0.37,HEIGHT * 0.65, 350,60)

    def display(self):
        self.font_Expsurface = self.fontExp.render(f'SCORE:{int(self.player.exp)}', False, TEXT_COLOR)


        self.game_paused = True

        pygame.draw.rect(self.display_surface,UI_BG_COLOR,self.rect)
        pygame.draw.rect(self.display_surface, TEXT_COLOR, self.rect,4)
        self.display_surface.blit(self.font_surface,self.font_rect)

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, self.Exprect)
        pygame.draw.rect(self.display_surface, TEXT_COLOR, self.Exprect, 4)
        self.display_surface.blit(self.font_Expsurface, self.font_Exprect)

