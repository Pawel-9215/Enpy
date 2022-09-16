import pygame
from settings import *

class UI:
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        #bar setup
        self.health_bar_rect = pygame.Rect(16, RESOLUTION[1] - 20, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(16, RESOLUTION[1] - 10, ENERGY_BAR_WIDTH, BAR_HEIGHT)

    def show_bar(self, current, max_amount, bg_rect, color):
        pass

    def display(self, player):
        pygame.draw.rect(self.display_surface, HEALTH_COLOR, self.health_bar_rect)