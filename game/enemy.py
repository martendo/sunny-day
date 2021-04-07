import pygame
from game.actor import Actor
from game.player import Player

class Enemy(Actor):
    layer = 0
    
    def __init__(self, *args):
        super().__init__(*args)
        
        # Don't do anything until it first appears on-screen
        self.enabled = False
    
    def update_enablement(self):
        if not self.enabled and self.rect.colliderect(pygame.Rect(
                self.game.map.camera.pos,
                (self.game.WIDTH_PX, self.game.HEIGHT_PX))):
            self.enabled = True
    
    def hit_actor(self, actor):
        if isinstance(actor, Player):
            if actor.is_stomping(self):
                self.kill()
                actor.bounce()
            else:
                actor.hurt()
        else:
            self.hit_enemy()


from game.enemies.renky import Renky
from game.enemies.ponko import Ponko
from game.enemies.booto import Booto

TYPES = {
    "Renky": Renky,
    "Ponko": Ponko,
    "Booto": Booto,
}
