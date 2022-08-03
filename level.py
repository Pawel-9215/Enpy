import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug

class Level:
    def __init__(self) -> None:
        
        self.display_surface = pygame.display.get_surface()
        
        #sprite groups setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        
        #sprite setup
        self.create_map()
        
    def create_map(self):
        
        for row_index, row in enumerate(WORLD_MAP):
            for column_index, column in enumerate(row):
                x = column_index*TILE_SIZE
                y = row_index*TILE_SIZE
                if column == 'x':
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                if column == 'p':
                   self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites)
            
        
    def run(self):
        self.visible_sprites.custom_draw()
        self.visible_sprites.update()
        debug(self.player.direction)
        #update and run the game
        pass
    
class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        
    def custom_draw(self):
        for sprite in self.sprites():
            self.display_surface.blit(sprite.image, sprite.rect)