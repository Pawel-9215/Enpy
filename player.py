from ntpath import join
import pygame
from settings import *
from support import import_folder
import os
from debug import debug
from enum import Enum

class State(Enum):
    MOVE = 1
    ATTACK = 2
    DEAD = 3

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites) -> None:
        super().__init__(groups)
        self.tile_size = 16
        self.image = pygame.image.load('./gfx/player/down_idle/down_idle_001.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-4, -8)
        self.hitbox.bottom = self.rect.bottom

        self.frame_index = 0
        self.animation_speed = 0.15

        #graphics setup
        self.import_player_assets()
        self.facing = "down"
        self.status = 'down_move'

        self.direction = pygame.math.Vector2()
        self.speed = 2
        
        self.state = State.MOVE

        #self.attacking = False #deprecated
        self.attack_cooldown = 400
        self.attack_time = None

        self.obstacle_sprites = obstacle_sprites

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
            print('attack')

        #magic input
        if keys[pygame.K_LCTRL]:
            #self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            print('magic')

    def get_status(self):
        #idle
        if self.state == State.MOVE:
            if self.direction.x == 0 and self.direction.y == 0:

                self.status = self.facing + "_" + "idle"
            else:

                self.status = self.facing + "_" + "move"

        elif self.state == State.ATTACK:

                self.status = self.facing + "_" + "attack"


    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # self.rect.center += self.direction * speed
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.midbottom = self.hitbox.midbottom

        if self.direction.x > 0:
            self.facing = "right"
        elif self.direction.x < 0:
            self.facing = "left"
        elif self.direction.y < 0:
            self.facing = "up"
        elif self.direction.y > 0:
            self.facing = "down"

        debug("\n\n"+str(self.direction))

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.state == State.ATTACK:
            if current_time - self.attack_time >= self.attack_cooldown:
                #self.attacking = False
                self.change_state(State.MOVE)

    def animate(self):
        animation = self.animations[self.status]

        #loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]

    def change_state(self, state: State):
        self.state = state

    def update(self):
        match self.state:
            case State.MOVE:
                self.move_state()
            case State.ATTACK:
                self.attack_state()
            case State.DEAD:
                self.dead_state()

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

