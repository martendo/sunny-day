import pygame
from game.animation import Animation
from game.enemy import Enemy

class Booto(Enemy):
    SPEED = 0.75
    
    HITBOX = pygame.Rect(
        2, 4,
        14, 12,
    )
    
    IMG_WIDTH = 16
    IMG_HEIGHT = 16
    SPRITESHEET = "enemies/booto"
    
    MOVING_ANIMATION_SETTINGS = {
        "img": (
            0,
            1,
            2,
            1,
            0,
            3,
            4,
            3,
        ),
        "duration": 50,
    }
    
    def __init__(self, game, pos):
        super().__init__(game, self.HITBOX, pos)
        
        self.animation = Animation(self, self.game, self.MOVING_ANIMATION_SETTINGS)
        self.image = self.animation.get_image()
        self.set_rect(self.image.get_rect())
        
        self.set_speed()
    
    def turn_around(self):
        self.direction = -self.direction
        self.set_speed()
    def set_speed(self):
        self.vel.x = self.SPEED * self.direction
    
    def update(self):
        self.update_enablement()
        if not self.enabled:
            return
        
        super().update()
        
        if self.blockcollided.x or self.game.at_edge(self):
            self.turn_around()
        
        self.animation.update()
    
    def hit_enemy(self):
        self.turn_around()
