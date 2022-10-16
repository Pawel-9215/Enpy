import pygame
from debug import *
from support import lerp, move_towards

class Entity(pygame.sprite.Sprite):
    def __init__(self, *groups) -> None:
        super().__init__(*groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()
        self.current_movement = pygame.math.Vector2()
        self.facing = "down"
        self.current_speed = 0.0
        self.acceleration = 0.1
        self.friction = 0.1
        self.active_triggers = []
        

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        self.current_movement.x = move_towards(self.current_movement.x, self.direction.x, self.acceleration, 0.1)
        self.current_movement.y = move_towards(self.current_movement.y, self.direction.y, self.acceleration, 0.1)
        
        # self.rect.center += self.direction * speed
        self.fractional_position[0] += self.current_movement.x * self.speed
        self.fractional_position[1] += self.current_movement.y * self.speed
        
        self.hitbox.x = self.fractional_position[0]
        self.collision('horizontal')
        self.hitbox.y = self.fractional_position[1]
        self.collision('vertical')
        self.rect.midbottom = self.hitbox.midbottom

        if self.direction.x > 0.5:
            self.facing = "right"
        elif self.direction.x < -0.5:
            self.facing = "left"
        elif self.direction.y < 0:
            self.facing = "up"
        elif self.direction.y > 0:
            self.facing = "down"

        #debug("\n\n"+str(self.direction))

    def trigger_detect(self):
        for sprite in self.trigger_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                self.active_triggers.append(sprite)
                # print("Trigger Activated!")
                sprite.trigger()
        for sprite in self.active_triggers:
            if not sprite.hitbox.colliderect(self.hitbox):
                sprite.armed = True
                self.active_triggers.remove(sprite)
                
    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.current_movement.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                        self.current_movement.x = 0
                    elif self.current_movement.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right
                        self.current_movement.x = 0
                    self.fractional_position = [self.hitbox.x, self.hitbox.y]

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.current_movement.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                        self.current_movement.y = 0
                    if self.current_movement.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom
                        self.current_movement.y = 0
                    self.fractional_position = [self.hitbox.x, self.hitbox.y]