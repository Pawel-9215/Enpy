#For the love of god...
import pygame, sys
from pygame.locals import *

print("Prepare for launch!")

#setup pygame
pygame.init()

#window
WIDTH, HEIGHT = 540, 480
RESOLUTION = (WIDTH, HEIGHT)

window_surface = pygame.display.set_mode(RESOLUTION, 0, 32)
pygame.display.set_caption("Hello World! :P")

#colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (235, 5, 5)
GREEN = (5, 235, 5)
BLUE = (5, 5, 235)

#fonts
base_font = pygame.font.SysFont(None, 32)

#set text
text = base_font.render('Hello World!', True, BLACK, BLUE)
textRect = text.get_rect()
textRect.centerx = window_surface.get_rect().centerx
textRect.centery = window_surface.get_rect().centery

#Draw BG
window_surface.fill(WHITE)

#draw poly
pygame.draw.polygon(window_surface, GREEN, ((146, 0), (291, 106), (236, 377), (56, 277), (0, 106)))

#draw some bullshit
pygame.draw.line(window_surface, BLUE, (4, 5), (530, 470), 4)
pygame.draw.line(window_surface, BLUE, (40, 15), (530, 70), 2)
pygame.draw.circle(window_surface, RED, (230, 240), 80)

window_surface.blit(text, textRect)

pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()