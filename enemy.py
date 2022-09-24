import pygame
from settings import *
from monster_data import *
from entity import Entity
from support import *

class Enemy(Entity):
    def __init__(self, monster_name, pos, *groups) -> None:
        super().__init__(*groups)
        self.sprit_type = 'enemy'
        self.name = monster_name

        #graphic setup
        self.import_graphics()
        self.status = 'idle'
        self.image = pygame.Surface((16,16))
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-4, -8)
        self.hitbox.bottom = self.rect.bottom

    def import_graphics(self):

        self.animations = {'up_move':[], 'down_move':[], 'left_move':[], 'right_move':[],
            'right_idle':[], 'left_idle':[], 'up_idle':[], "down_idle":[],
            'right_attack': [], 'left_attack': [], 'up_attack':[], 'down_attack':[], 
            'dead':[]}

        main_path = f'./gfx/monsters/{self.name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)
