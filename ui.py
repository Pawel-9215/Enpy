import pygame
from settings import *

class UI:
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        #bar setup
        self.health_bar_rect = pygame.Rect(16+54, RESOLUTION[1] - (18+16), HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(16+46, RESOLUTION[1] - (9+16), ENERGY_BAR_WIDTH, BAR_HEIGHT//2)
        self.exp_bar_rect = pygame.Rect(16+55, RESOLUTION[1]-(20+16), EXP_BAR_WIDTH, BAR_HEIGHT//4)

        self.hud_img = pygame.image.load('./gfx/ui/ui_main_hud.png').convert_alpha()

        self.weapon_graphics = []

        for weapon in weapon_data.values():
            path = weapon['graphic']+"Sprite.png"
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)

    def show_bar(self, current, max_amount, bg_rect, color):
        #draw bg
        pygame.draw.rect(self.display_surface, BAR_BG_COLOR, bg_rect)

        #convert data to pixel amount

        ratio = current / max_amount
        current_width = ratio * bg_rect.width
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        pygame.draw.rect(self.display_surface, color, current_rect)

    def weapon_selection(self, weapon_index):
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center = (23+16, RESOLUTION[1] - (23+16)))

        self.display_surface.blit(weapon_surf, weapon_rect)


    def display(self, player):
        #health bar
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)
        self.show_bar(player.exp, player.next_level, self.exp_bar_rect, EXP_POINT_COLOR)

        hud_height = self.hud_img.get_size()[1]
        self.display_surface.blit(self.hud_img, (16, RESOLUTION[1]-16-hud_height))

        self.weapon_selection(player.weapon_index)