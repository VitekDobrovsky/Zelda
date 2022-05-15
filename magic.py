import pygame
from settings import *

class MagicPl:
    def __init__(self,animation_player):
        self.animation_player = animation_player

    def heal(self,player,strength,cost,groups):
        if player.energy >= cost and not player.health >= player.stats['health']:
            if not cost >= player.energy:
                player.health += strength
                player.energy -= cost
                self.animation_player.create_particles('aura',player.rect.center,groups)
                self.animation_player.create_particles('heal', player.rect.center - pygame.math.Vector2(0,30), groups)
                if player.health >= player.stats['health']:
                    player.health = player.stats['health']

    def flame(self):
        print('flame')