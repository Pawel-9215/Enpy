import pygame
from settings import *
from tile import Tile, BottomTile, TriggerTile, WaterTile
from player import Player
from debug import debug
from pytmx.util_pygame import load_pygame
from weapon import Weapon
from ui import UI
from water import Water
from enemy import Enemy


class Level:
    def __init__(self, engine, map) -> None:

        self.player = None
        self.display_surface = pygame.display.get_surface()
        self.engine = engine

        # sprite groups setup
        self.ground_sprites = CameraGroup()
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.trigger_sprites = pygame.sprite.Group()

        #attack sprites
        self.current_attack = None

        self.attack_sprites = pygame.sprite.Group()
        self.target_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map(map)

        #user interface
        self.ui = UI()

    def create_map(self, level):
        """_summary_
        Load tmx file from map generated using Tiled
        """
        tmx_data = load_pygame(f'./maps/{level}.tmx')
        self.lvl_width = tmx_data.width*TILE_SIZE
        self.lvl_height = tmx_data.height*TILE_SIZE

        for layer in tmx_data.visible_layers:
            if layer.name in ('base_ground', 'base_ground_elements'):
                for x, y, surf in layer.tiles():
                    Tile((x*TILE_SIZE, y*TILE_SIZE), (self.ground_sprites), surf)
            elif layer.name in ('plants_and_rocks'):
                for x, y, surf in layer.tiles():
                    BottomTile((x*TILE_SIZE, y*TILE_SIZE), (self.visible_sprites), surf)
            elif layer.name in ('base_ground_blocking'):
                for x, y, surf in layer.tiles():
                    Tile((x*TILE_SIZE, y*TILE_SIZE), (self.visible_sprites, self.obstacle_sprites), surf)
            elif layer.name == 'large_blockers':
                #print(layer)
                for x, y, surf in layer.tiles():
                   Tile((x*TILE_SIZE, y*TILE_SIZE), (self.obstacle_sprites), surf)
            elif layer.name == 'water':
                for x, y, surf in layer.tiles():
                    self.ground_sprites.water_group.append(Water((x*TILE_SIZE, y*TILE_SIZE)))

        for obj in tmx_data.objects:
            if obj.name == "player_start":
                self.player = Player((obj.x, obj.y), 
                        self.visible_sprites, 
                        self.obstacle_sprites, 
                        self.trigger_sprites,
                        self.create_attak, 
                        self.end_attack,
                        self.create_magic)
            elif obj.name == "undead":
                Enemy(obj.name, (obj.x, obj.y), self.obstacle_sprites, self.trigger_sprites, [self.visible_sprites, self.target_sprites])
            elif obj.name in ['building', 'house']:
                BottomTile((obj.x, obj.y), self.visible_sprites, surf = obj.image)
            elif obj.name == "blocker":
                Tile((obj.x, obj.y), self.obstacle_sprites, surf = obj.image)
            elif obj.name == 'tree':
                BottomTile((obj.x, obj.y), self.visible_sprites, surf = obj.image)
            elif obj.name == 'level_trigger':
                TriggerTile((obj.x, obj.y), [self.trigger_sprites, self.visible_sprites], self.change_map, None, obj.image)

    def create_attak(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def change_map(self):
        print('Level function - change level')
        self.engine.running = False
        self.engine.level = Level(self.engine, 'combat_tests')
        self.engine.running = True
        del self

    def end_attack(self):
        if self.current_attack:
            self.current_attack.kill()
            print('attack finished')
        self.current_attack = None
        
    def create_magic(self, style, strength, cost):
        print(style)
        print(strength)
        print(cost)

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.target_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def run(self):

        self.ground_sprites.custom_draw(self.player, (self.lvl_width, self.lvl_height))
        self.visible_sprites.custom_draw(self.player, (self.lvl_width, self.lvl_height))
        self.visible_sprites.update()
        self.player_attack_logic()
        #debug(self.player.direction)
        # update and run the game
        #debug(self.player.status)
        self.ui.display(self.player)
        pass
        

class CameraGroup(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        self.water_group = []

    def water_draw(self, player, offset):

        #for sprite in self.sprites():
        for water in self.water_group:
            if (water.position - pygame.Vector2(player.rect.center)).length() < RENDER_DIST//2:
                water.update()
                water.render(self.offset, self.display_surface)

    def custom_draw(self, player, bounds):
        
        # getting offset from player
        if 0 + RESOLUTION[0]//2 < player.rect.centerx < bounds[0] - RESOLUTION[0]//2:
            self.offset.x = player.rect.centerx - self.half_width

        if 0 + RESOLUTION[1]//2 < player.rect.centery < bounds[1] - RESOLUTION[1]//2:
            self.offset.y = player.rect.centery - self.half_height

        self.water_draw(player, self.offset)

        #for sprite in self.sprites():
        for sprite in self.sprites():
            if (pygame.Vector2(sprite.rect.center) - pygame.Vector2(player.rect.center)).length() < RENDER_DIST:
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

    def custom_draw(self, player, bounds):

        # getting offset from player
        if 0 + RESOLUTION[0]//2 < player.rect.centerx < bounds[0] - RESOLUTION[0]//2:
            self.offset.x = player.rect.centerx - self.half_width

        if 0 + RESOLUTION[1]//2 < player.rect.centery < bounds[1] - RESOLUTION[1]//2:
            self.offset.y = player.rect.centery - self.half_height

        #for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.hitbox.centery):
            if (pygame.Vector2(sprite.rect.center) - pygame.Vector2(player.rect.center)).length() < RENDER_DIST:
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)
