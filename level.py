import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from pytmx.util_pygame import load_pygame


class Level:
    def __init__(self) -> None:

        self.player = None
        self.display_surface = pygame.display.get_surface()

        # sprite groups setup
        self.ground_sprites = CameraGroup()
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

    def create_map(self):
        """_summary_
        Load tmx file from map generated using Tiled
        """
        tmx_data = load_pygame('./maps/base_map.tmx')

        for layer in tmx_data.visible_layers:
            if layer.name in ('base_ground', 'road'):
                for x, y, surf in layer.tiles():
                    Tile((x*TILE_SIZE, y*TILE_SIZE), (self.ground_sprites), surf)
            elif layer.name in ('plants_and_rocks', 'buildings'):
                for x, y, surf in layer.tiles():
                    Tile((x*TILE_SIZE, y*TILE_SIZE), (self.visible_sprites), surf)
            elif layer.name in ('blockers'):
                for x, y, surf in layer.tiles():
                    Tile((x*TILE_SIZE, y*TILE_SIZE), (self.obstacle_sprites), surf)

        for obj in tmx_data.objects:
            if obj.name == "player_start":
                self.player = Player((obj.x, obj.y), self.visible_sprites, self.obstacle_sprites)

    def run(self):

        self.ground_sprites.custom_draw(self.player)
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        #debug(self.player.direction)
        # update and run the game
        debug(self.player.status)
        pass
        

class CameraGroup(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):

        # getting offset from player
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        #for sprite in self.sprites():
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
            sprite.animate()


class YSortCameraGroup(CameraGroup):
    def __init__(self) -> None:
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):

        # getting offset from player
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        #for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.hitbox.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
