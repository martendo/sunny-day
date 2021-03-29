import pygame
from game.actor import Actor

# TODO: Make enemies!!!

class Enemy(Actor):
    HITBOX = (
        0, 0,
        8, 8,
    )
    
    def __init__(self, *args):
        super().__init__(*args, self.HITBOX)
        
        self.image = pygame.Surface((self.game.TILE_SIZE, self.game.TILE_SIZE))
        self.image.fill(self.game.PLACEHOLDER_COLOUR)
        self.rect = self.image.get_rect()
        
        self.vel.x = 1

TYPES = (
    Enemy,
)
