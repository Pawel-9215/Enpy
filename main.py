import pygame
from pygame.locals import *
import sys

from level import Level
from settings import *
from debug import debug
from profilehooks import profile


class Engine:
    """Main game class sitting on top of everything else
    """

    def __init__(self) -> None:

        # general setup for pygameq
        self.screen = pygame.display.set_mode(RESOLUTION, HWSURFACE|DOUBLEBUF|RESIZABLE|SCALED)
        self.clock = pygame.time.Clock()
        self.level = Level(self, 'ruins_1')
        self.running = True

        pygame.display.set_caption(TITLE)
        
    @profile
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
            self.screen.fill('#3D897B')
            if self.running:
                self.level.run()
            debug(self.clock.get_fps())
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Engine()
    game.run()
