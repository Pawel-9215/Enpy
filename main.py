import pygame, sys
from settings import *
from debug import debug
from level import Level

class Engine:
    """Main game class sitting on top of everythiong else
    """
    def __init__(self) -> None:
        
        #generas setup for pygame
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
            pygame.display.update()
            self.clock.tick(FPS)
   
if __name__ == '__main__':
    game = Engine()
    game.run()