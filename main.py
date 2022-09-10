import pygame
import sys

from level import Level
from settings import *
from debug import debug


class Engine:
    """Main game class sitting on top of everything else
    """

    def __init__(self) -> None:

        # general setup for pygame
        self.screen = pygame.display.set_mode(RESOLUTION)
        self.clock = pygame.time.Clock()
        self.level = Level()

        pygame.display.set_caption(TITLE)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill('black')
            self.level.run()
            #debug(self.clock.get_fps())
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Engine()
    game.run()
