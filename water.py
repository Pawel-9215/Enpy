import pygame
import random
from settings import *

class Water():
    def __init__(self, pos) -> None:
        self.position = pygame.Vector2(pos)
        self.base_water_color = '#3D897B'
        self.high_light_color = '#6DBDAF'


        self.populate()

    def populate(self):
        pass

    def wave(self):
        pass

    def update(self):
        pass

    def render(self, offset, display):
        pass