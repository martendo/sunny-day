import pygame
from random import randint, choice
from game.animation import Animation
from game.enemy import Enemy

class Renky(Enemy):
    SPEED = 0.5
    
    HITBOX = pygame.Rect(
        4, 8,
        8, 8,
    )
    
    MOVING_ANIMATION_SETTINGS = {
        "img": (
            "renky-m-1",
            "renky-m-2",
            "renky-m-1",
            "renky-m-3",
        ),
        "lengths": 3,
    }
    
    def __init__(self, *args):
        super().__init__(*args, self.HITBOX)
        
        self.animation = Animation(self, self.game, self.MOVING_ANIMATION_SETTINGS)
        self.image = self.animation.get_image()
        self.rect = self.image.get_rect()
        
        self.vel.x = self.SPEED * self.direction
    
    def update(self):
        super().update()
        
        if self.blockcollided[0]:
            self.direction = -self.direction
            self.vel.x = self.SPEED * self.direction
        
        self.animation.update()
