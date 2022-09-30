from ntpath import join
import pygame
from settings import *
from support import import_folder
import os
from debug import debug
from enum import Enum
from entity import Entity

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, end_attack, create_magic) -> None:
        super().__init__(groups)
        self.sprite_type = 'player'
        self.tile_size = 16
        self.image = pygame.image.load('./gfx/player/down_idle/down_idle_001.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-4, -8)
        self.hitbox.bottom = self.rect.bottom
        self.fractional_position = [self.hitbox.x, self.hitbox.y]
        self.buttons_pressed = []

        #graphics setup
        self.import_player_assets()
        self.facing = "down"
        self.status = 'down_move'

        self.state = State.MOVE

        #self.attacking = False #deprecated
        self.attack_time = None
        self.create_attack = create_attack
        self.end_attack = end_attack

        self.obstacle_sprites = obstacle_sprites

        #equipment
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.attack_cooldown = 300 + weapon_data[self.weapon]['cooldown']

        #magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.create_magic = create_magic

        #stats
        self.stats = {'health': 100, 
                'energy': 60, 
                'attack': 10, 
                'magic': 6, 
                'speed': 2}

        self.health = self.stats['health'] // 2
        self.energy = self.stats['energy'] // 2
        self.exp = 12
        self.next_level = 18
        self.speed = self.stats['speed']


    def import_player_assets(self):
        character_path = './gfx/player'

        #walking = pygame.image.load(os.path.join(character_path, "Walk.png")).convert_alpha()

        self.animations = {'up_move':[], 'down_move':[], 'left_move':[], 'right_move':[],
            'right_idle':[], 'left_idle':[], 'up_idle':[], "down_idle":[],
            'right_attack': [], 'left_attack': [], 'up_attack':[], 'down_attack':[], 
            'dead':[]}

        for animation in self.animations:
            full_path = os.path.join(character_path, animation)
            self.animations[animation] = import_folder(full_path)
        #print(self.animations)

    def input(self):
        keys = pygame.key.get_pressed()

        #movement input
        if keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN] and not keys[pygame.K_UP]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        #attack input
        if keys[pygame.K_SPACE]:
            
            self.attack_time = pygame.time.get_ticks()
            self.change_state(State.ATTACK)
            self.create_attack()

        #magic input
        if keys[pygame.K_LCTRL] and pygame.K_LCTRL not in self.buttons_pressed:
            self.buttons_pressed.append(pygame.K_LCTRL)
            #self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.create_magic(self.magic, 
                    magic_data[self.magic]['strength']+self.stats['magic'], 
                    magic_data[self.magic]['cost'])

        elif not keys[pygame.K_LCTRL] and pygame.K_LCTRL in self.buttons_pressed:
            self.buttons_pressed.remove(pygame.K_LCTRL)

        #toggle weapon
        if keys[pygame.K_q] and pygame.K_q not in self.buttons_pressed:
            
            self.buttons_pressed.append(pygame.K_q)
            print('toggle weapon')
            weapon_amount = len(list(weapon_data.keys()))
            self.weapon_index += 1
            if self.weapon_index >= weapon_amount:
                self.weapon_index = 0
            self.weapon = list(weapon_data.keys())[self.weapon_index]

            self.attack_cooldown = weapon_data[self.weapon]['cooldown']+300-self.speed

        elif not keys[pygame.K_q] and pygame.K_q in self.buttons_pressed:
            self.buttons_pressed.remove(pygame.K_q)

        #toggle magic
        if keys[pygame.K_e] and pygame.K_e not in self.buttons_pressed:
            
            self.buttons_pressed.append(pygame.K_e)
            print('toggle magic')
            magic_amount = len(list(magic_data.keys()))
            self.magic_index += 1
            if self.magic_index >= magic_amount:
                self.magic_index = 0
            self.magic = list(magic_data.keys())[self.magic_index]

        elif not keys[pygame.K_e] and pygame.K_e in self.buttons_pressed:
            self.buttons_pressed.remove(pygame.K_e)
            

    def get_status(self):
        #idle
        if self.state == State.MOVE:
            if self.direction.x == 0 and self.direction.y == 0:

                self.status = self.facing + "_" + "idle"
            else:

                self.status = self.facing + "_" + "move"

        elif self.state == State.ATTACK:

                self.status = self.facing + "_" + "attack"

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.state == State.ATTACK:
            if current_time - self.attack_time >= self.attack_cooldown:
                #self.attacking = False
                self.change_state(State.MOVE)
                self.end_attack()

    def animate(self):
        animation = self.animations[self.status]

        #loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]

    def get_full_weapon_damage(self):
        full_damage = self.stats['attack'] + weapon_data[self.weapon]['damage']

        return full_damage

    def change_state(self, state: State):
        self.state = state

    def update(self):
        #debug(self.hitbox.center)
        match self.state:
            case State.MOVE:
                self.move_state()
            case State.ATTACK:
                self.attack_state()
            case State.DEAD:
                self.dead_state()
        debug(self.direction)
        self.animate()

    def move_state(self):
        self.input()
        self.move(self.speed)
        self.cooldowns()
        self.get_status()

    def attack_state(self):
        #self.input()
        
        self.cooldowns()
        self.get_status()

    def dead_state(self):
        pass

