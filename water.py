import pygame
import random
from settings import *

class Water():
    def __init__(self, pos) -> None:
        self.position = pygame.Vector2(pos)
        self.base_water_color = '#3D897B'
        self.water_colors = ['#49A188', '#40978D', '#5B8F81', '#4E9D9E', '#52958A', '#46947B']
        self.hilight = '#6DBDAF'
        self.my_color = self.water_colors[random.randint(0, len(self.water_colors)-1)]
        self.displacement = 32 + random.randint(-4, 4)

        #animation
        self.max_wave = 24
        self.annimation_speed = random.randint(40, 90)* 0.01
        self.anim_mod = random.randint(15, 25)*0.1
        self.anim_frame = 0
        self.frame_speed = random.randint(10, 25)*0.01
        self.thickness = random.randint(1, 3)

        self.thins = random.randint(1,3)

        self.hi_off = pygame.Vector2(-64, 6)
        self.low_off = pygame.Vector2(64, -6)
        
        self.points = []
        self.direction = [random.randint(0, 1)]

        self.populate()

    def populate(self):

        full_lenght = random.randint(6, 16)
        step = (TILE_SIZE // full_lenght) * 6
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
        self.anim_frame += 0.15
        if self.anim_frame >= 1:
            self.wave()
            self.propagate()
            self.anim_frame = 0

    def render(self, offset, display):
        
        
        for i in range(0, len(self.points)-2, 2):
            #pygame.draw.circle(display, self.my_color, self.points[i]-offset, 32)
            pygame.draw.line(display, self.my_color, self.points[i]-offset, self.points[i+2]-offset, self.thickness)

            pygame.draw.line(display, self.hilight, self.points[i]-offset+self.low_off, self.points[i+2]-offset+self.low_off, self.thins)
            pygame.draw.line(display, self.hilight, self.points[i]-offset+self.hi_off, self.points[i+2]-offset+self.hi_off, self.thins)