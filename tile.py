import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, surf = pygame.Surface((TILE_SIZE, TILE_SIZE))) -> None:
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect

    def animate(self):
        pass

class WaterTile(Tile):
    def __init__(self, pos, groups, surf=pygame.Surface((TILE_SIZE, TILE_SIZE))) -> None:
        super().__init__(pos, surf, groups)
        self.frame = 0
    
    def animate(self):
        if self.frame >= 60:
            self.frame = 0
        else:
            self.frame += 1

        if self.frame % 10 == 0:
            self.scroll()

    def scroll(self):
        self.image.scroll(64, 0)

