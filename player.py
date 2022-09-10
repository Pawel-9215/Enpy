from ntpath import join
import pygame
from settings import *
from support import import_folder
import os
from debug import debug


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites) -> None:
        super().__init__(groups)
        self.tile_size = 16
        self.image = pygame.image.load('./gfx/test/player1.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-16, -32)
        self.hitbox.bottom = self.rect.bottom

        #graphics setup
        self.import_player_assets()
        self.status = 'down'

        self.direction = pygame.math.Vector2()
        self.speed = 4

        self.state = {1: "move"}
        self.attack_cooldown = 400
        self.attack_time = None

        self.obstacle_sprites = obstacle_sprites

    def import_player_assets(self):
        character_path = './gfx/player'

        #walking = pygame.image.load(os.path.join(character_path, "Walk.png")).convert_alpha()

        self.animations = {'up':[], 'down':[], 'left':[], 'right':[],
            'right_idle':[], 'left_idle':[], 'up_idle':[], "down_idle":[],
            'right_attack': [], 'left_attack': [], 'up_attack':[], 'down_attack':[]}

        for animation in self.animations:
            full_path = os.path.join(character_path, animation)
            self.animations[animation] = import_folder(full_path)
        #print(self.animations)

    def input(self):
        keys = pygame.key.get_pressed()

        #movement input
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = "up"
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = "down"
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        else:
            self.direction.x = 0

        #attack input
        if keys[pygame.K_SPACE] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            print('attack')

        #magic input
        if keys[pygame.K_LCTRL] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            print('magic')

    def get_status(self):
        #idle
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not "attack" in self.status:
                self.status = self.status+ "_idle"

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status and not 'idle' in self.status:
                self.status = self.status+ "_attack"

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # self.rect.center += self.direction * speed
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.midbottom = self.hitbox.midbottom

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

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False


    def update(self):
        self.input()
        self.move(self.speed)
        self.cooldowns()
        self.get_status()
