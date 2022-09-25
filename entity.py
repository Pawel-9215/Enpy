import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, *groups) -> None:
        super().__init__(*groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()
        self.facing = "down"
        

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # self.rect.center += self.direction * speed
        self.fractional_position[0] += self.direction.x * speed
        self.fractional_position[1] += self.direction.y * speed
        self.hitbox.x = self.fractional_position[0]
        self.collision('horizontal')
        self.hitbox.y = self.fractional_position[1]
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

        #debug("\n\n"+str(self.direction))


    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right
                    self.fractional_position = [self.hitbox.x, self.hitbox.y]

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom
                    self.fractional_position = [self.hitbox.x, self.hitbox.y]