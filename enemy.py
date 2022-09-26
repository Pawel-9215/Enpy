import pygame
from settings import *
from monster_data import *
from entity import Entity
from support import *
from debug import *

class Enemy(Entity):
    def __init__(self, monster_name, pos, obstacle_sprites, *groups) -> None:
        super().__init__(*groups)
        self.sprite_type = 'enemy'
        self.name = monster_name
        self.obstacle_sprites = obstacle_sprites
        for group in groups[0]:
            for sprite in group:
                if sprite.sprite_type == 'player':
                    # print('found player!')
                    self.player = sprite

        #movement_animation
        self.facing = 'down'
        self.status = 'down_idle'
        self.state = State.MOVE

        #graphic setup
        self.import_graphics()
        self.image = self.animations[self.status][int(self.frame_index)]
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-4, -8)
        self.hitbox.bottom = self.rect.bottom
        self.fractional_position = [self.hitbox.x, self.hitbox.y]


        #enemy_stats
        self.attack_time = None
        self.enemy_stats = monster_data[self.name]

        self.attack_cooldown = self.enemy_stats['speed'] * 200
        self.health = self.enemy_stats['health']
        self.exp = self.enemy_stats['exp']
        self.damage = self.enemy_stats['damage']
        self.attack_type = self.enemy_stats['attack_type']
        self.speed = self.enemy_stats['speed']
        self.resistance = self.enemy_stats['resistance']
        self.attack_radius = self.enemy_stats['attack_radius']
        self.notice_radius = self.enemy_stats['notice_radius']


        

    def import_graphics(self):

        self.animations = {'up_move':[], 'down_move':[], 'left_move':[], 'right_move':[],
            'right_idle':[], 'left_idle':[], 'up_idle':[], "down_idle":[],
            'right_attack': [], 'left_attack': [], 'up_attack':[], 'down_attack':[], 
            'dead':[]}

        main_path = f'./gfx/monsters/{self.name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def get_status(self):
        #idle
        if self.state == State.MOVE or self.state == State.FOLLOW:
            if self.direction.x == 0 and self.direction.y == 0:

                self.status = self.facing + "_" + "idle"
            else:

                self.status = self.facing + "_" + "move"

        elif self.state == State.ATTACK:

                self.status = self.facing + "_" + "attack"

    def get_action(self):
        distance_to_player = self.get_distance_to_player()[0]

        if distance_to_player <= self.attack_radius and self.state is not State.ATTACK:
            print("bah bah!")
            self.attack_time = pygame.time.get_ticks()
            self.change_state(State.ATTACK)

        elif distance_to_player <= self.notice_radius and self.state is not State.FOLLOW:
            self.change_state(State.FOLLOW)
            print("gotha!")

        elif  distance_to_player > self.notice_radius and self.state is not State.MOVE:
            self.change_state(State.MOVE)

        else:
            pass

    def get_distance_to_player(self):
        player_vec = pygame.math.Vector2(self.player.hitbox.center) - pygame.math.Vector2(self.hitbox.center)
        distance = player_vec.magnitude()
        if distance > 0:
            direction = player_vec.normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance, direction)


    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.state == State.ATTACK:
            if current_time - self.attack_time >= self.attack_cooldown:
                #self.attacking = False
                self.change_state(State.MOVE)
                #self.end_attack() 

    def animate(self):
        animation = self.animations[self.status]

        #loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]

    def update(self):
        # debug(self.status)
        match self.state:
            case State.MOVE:
                self.move_state()
            case State.ATTACK:
                self.attack_state()
            case State.DEAD:
                self.dead_state()
            case State.FOLLOW:
                self.follow_state()

        self.animate()

    def move_state(self):
        self.direction = pygame.math.Vector2()
        self.move(self.speed)
        # self.cooldowns()
        self.get_status()
        self.get_action()

    def attack_state(self):
        self.get_status()
        self.cooldowns()

    def dead_state(self):
        pass

    def follow_state(self):
        self.direction = self.get_distance_to_player()[1]
        self.move(self.speed)
        #print(self.direction)
        self.get_action()
        self.get_status()

    def change_state(self, state: State):
        self.state = state
