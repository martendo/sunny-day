import pygame
from game.actor import Actor
from game import colour

# TODO: Make enemies!!!

class Enemy(Actor):
    HITBOX = (
        0, 0,
        8, 8,
    )
    
    def __init__(self, *args):
        super().__init__(*args, self.HITBOX)
        
        self.image = pygame.Surface((self.game.TILE_SIZE, self.game.TILE_SIZE))
        self.image.fill(colour.PLACEHOLDER)
        self.rect = self.image.get_rect()
        
        self.vel.x = 1

TYPES = (
    Enemy,
)
