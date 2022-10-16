import pygame
import random
from settings import *
import math

class Water():
    def __init__(self, pos) -> None:
        self.position = pygame.Vector2(pos)
        self.base_water_color = '#3D897B'
        self.high_light_color = '#6DBDAF'
        self.points = []


        self.populate()

    def populate(self):
        random.seed(None)
        #first_sin_input = random.randint(1,90)
        for i in range(2):
            point_xy = pygame.Vector2(self.position.x+random.randint(1, 8)+i*random.randint(3, 8), self.position.y+random.randint(2, 16))
            self.points.append([point_xy, random.randint(1,359)])

    def wave(self, point: pygame.Vector2, sin_input: int):
        
        speed = random.randint(1,2)
        sin_input += speed
        if sin_input >= 360:
            sin_input = 0

        point.y += (math.sin(math.radians(sin_input)))/random.randint(20,25)

        return sin_input

    def update(self):
        for point in self.points:
            point[1] = self.wave(point[0], point[1])

    def render(self, offset, display):
        for point in self.points:
            random_width = point[1]//100
            vector_width = pygame.Vector2(random_width, 0)
            pygame.draw.line(display, self.high_light_color, point[0]-offset-vector_width, point[0]-offset+vector_width)
'''
wat = Water((64,64))
tt = 0

while tt <= 900:
    tt += 1

    wat.update()
    print(wat.points[1])
    '''