import pygame
from time import time
from game.animation import Animation
from game.enemy import Enemy

class Ponko(Enemy):
    SPEED = 0.75
    
    HITBOX = pygame.Rect(
        0, 0,
        16, 8,
    )
    
    IMG_WIDTH = 16
    IMG_HEIGHT = 8
    SPRITESHEET = "enemies/ponko"
    
    MOVING_ANIMATION_SETTINGS = {
        "img": (
            0,
            1,
            0,
            2,
        ),
        "duration": 50,
    }
    IDLE_IMAGE = 0
    
    MOVE_TIME = 1
    
    def __init__(self, game, pos):
        super().__init__(game, self.HITBOX, pos)
        
        self.animation = Animation(self, self.game, self.MOVING_ANIMATION_SETTINGS)
        self.image = self.animation.get_image()
        self.set_rect(self.image.get_rect())
        
        self.moving = False
        self.cycle_end = time() + self.MOVE_TIME
    
    def turn_around(self):
        self.direction = -self.direction
        self.set_speed()
    def set_speed(self):
        if self.moving:
            self.vel.x = self.SPEED * self.direction
        else:
            self.vel.x = 0
    
    def update(self):
        self.update_enablement()
        if not self.enabled:
            return
        
        if time() >= self.cycle_end:
            self.moving = not self.moving
            self.set_speed()
            self.cycle_end += self.MOVE_TIME
            if not self.moving:
                self.image = self.game.SPRITESHEETS[self.SPRITESHEET][self.IDLE_IMAGE]
        
        if self.moving and (self.blockcollided.x or self.game.at_edge(self)):
            self.turn_around()
        
        super().update()
        
        if self.moving:
            self.animation.update()
    
    def hit_enemy(self):
        self.turn_around()
