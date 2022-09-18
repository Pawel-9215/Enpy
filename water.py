import pygame
import random
from settings import *

class Water():
    def __init__(self, pos) -> None:
        self.position = pygame.Vector2(pos)
        self.base_water_color = '#3D897B'
        self.displacement = 32 + random.randint(-4, 4)

        #animation
        self.max_wave = 24
        self.annimation_speed = random.randint(10, 40)* 0.01
        self.anim_mod = 2
        
        self.points = []
        self.direction = [random.randint(0, 1)]

        self.populate()

    def populate(self):

        full_lenght = random.randint(4, 8)
        step = (TILE_SIZE // full_lenght) * 2
        for i in range(full_lenght):
            self.points.append(pygame.Vector2(self.position.x + i*step, self.position.y+self.displacement))

    def wave(self):

        if self.direction[0] == 0:
            self.points[0].y -= self.annimation_speed * self.anim_mod
            if self.points[0].y <= self.position.y+self.displacement:
                self.anim_mod -= 0.1
            elif self.points[0].y >= self.position.y+self.displacement:
                self.anim_mod += 0.1
            if self.points[0].y <= self.position.y+self.displacement - self.max_wave:
                self.direction[0] = 1
                
        elif self.direction[0] == 1:
            self.points[0].y += self.annimation_speed * self.anim_mod
            if self.points[0].y >= self.position.y+self.displacement:
                self.anim_mod -= 0.1
            else:
                self.anim_mod += 0.1
            if self.points[0].y >= self.position.y+self.displacement + self.max_wave:
                self.direction[0] = 0

    def propagate(self):

        for i in range(len(self.points)-1, 0, -1):
            self.points[i].y = self.points[i-1].y

    def update(self):
        self.wave()
        self.propagate()

    def render(self, offset, display):
        
        
        for i in range(0, len(self.points)-1, 2):
            pygame.draw.circle(display, self.base_water_color, self.points[i]-offset, 5)
        #     pygame.draw.line(display, self.base_water_color, self.points[i]-offset, self.points[i+1]-offset, 4)