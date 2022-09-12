import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, *groups) -> None:
        super().__init__(*groups)
        self.direction = player.facing
        #print(self.direction)

        #graphic
        self.image = pygame.Surface((16,16))

        #placement
        match self.direction:
            case "down":
                self.rect = self.image.get_rect(top = player.rect.bottom)
            case "up":
                self.rect = self.image.get_rect(bottom = player.rect.top)
            case "left":
                self.rect = self.image.get_rect(right = player.rect.left)
            case "right":
                self.rect = self.image.get_rect(midleft = player.rect.midright)

        self.hitbox = self.rect