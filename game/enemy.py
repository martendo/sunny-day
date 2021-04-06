import pygame
from game.actor import Actor

class Enemy(Actor):
    layer = 0
    
    def __init__(self, *args):
        super().__init__(*args)
        
        # Don't do anything until it first appears on-screen
        self.enabled = False
    
    def update(self):
        if not self.enabled and self.rect.colliderect(pygame.Rect(
                self.game.map.camera.pos,
                (self.game.WIDTH_PX, self.game.HEIGHT_PX))):
            self.enabled = True
        
        if self.enabled:
            super().update()


from game.enemies.renky import Renky

TYPES = {
    "Renky": Renky,
}
