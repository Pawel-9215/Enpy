import pygame
from settings import *

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, *groups) -> None:
        super().__init__(*groups)
        self.direction = player.facing
        #print(self.direction)

        #graphic
        full_path = weapon_data[player.weapon]['graphic']+"SpriteInHand.png"
        self.image = pygame.image.load(full_path).convert_alpha()

        #placement
        match self.direction:
            case "down":
                self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.Vector2(-2, 0))
            case "up":
                self.image = pygame.transform.rotate(self.image, 180)
                self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.Vector2(-2, 0))
            case "left":
                self.image = pygame.transform.rotate(self.image, -90)
                self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.Vector2(0, 4))
            case "right":
                self.image = pygame.transform.rotate(self.image, 90)
                self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.Vector2(0, 4))

        self.hitbox = self.rect