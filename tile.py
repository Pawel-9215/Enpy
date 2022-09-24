import pygame
from settings import *
from support import import_folder
import random

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, surf = pygame.Surface((TILE_SIZE, TILE_SIZE))) -> None:
        super().__init__(groups)
        self.sprite_type = 'tile'
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect

    def animate(self):
        pass

class BottomTile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, surf = pygame.Surface((TILE_SIZE, TILE_SIZE))) -> None:
        super().__init__(groups)
        self.sprite_type = 'tile'
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-8, -(self.rect.height//2))
        self.hitbox.bottom = self.rect.bottom
        

    def animate(self):
        pass

class WaterTile(Tile):
    def __init__(self, pos, groups, surf=pygame.Surface((TILE_SIZE, TILE_SIZE))) -> None:
        super().__init__(pos, groups, surf)
        self.sprite_type = 'water'
        self.frame = 0
        self.import_water_assets()
        self.frame_index = random.randint(0, 3)
        self.animation_speed = random.randint(1, 10)*0.01

    def import_water_assets(self):
        water_path = './gfx/water'

        #walking = pygame.image.load(os.path.join(character_path, "Walk.png")).convert_alpha()

        self.animation = import_folder(water_path)
        #print(self.animations)
    
    def animate(self):
        animation = self.animation

        #loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]

    def scroll(self):
        self.image.scroll(64, 0)

    def update(self):
        self.animate()

