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

        #movement_animation
        self.facing = 'down'
        self.status = 'down_idle'

        #graphic setup
        self.import_graphics()
        self.image = self.animations[self.status][int(self.frame_index)]
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

    def animate(self):
        animation = self.animations[self.status]

        #loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]

    def change_state(self, state: State):
        self.state = state
