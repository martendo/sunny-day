import pygame
from game.animation import Animation
from game.enemy import Enemy
from game.player import Player

class Renky(Enemy):
    SPEED = 0.5
    
    HITBOX = pygame.Rect(
        4, 8,
        8, 8,
    )
    
    IMG_WIDTH = 16
    IMG_HEIGHT = 16
    SPRITESHEET = "enemies/renky"
    
    MOVING_ANIMATION_SETTINGS = {
        "img": (
            0,
            1,
            0,
            2,
        ),
        "duration": 100,
    }
    
    def __init__(self, game, pos):
        super().__init__(game, self.HITBOX, pos)
        
        self.animation = Animation(self, self.game, self.MOVING_ANIMATION_SETTINGS)
        self.image = self.animation.get_image()
        self.set_rect(self.image.get_rect())
        
        self.set_speed()
    
    def set_speed(self):
        self.vel.x = self.SPEED * self.direction
    
    def update(self):
        super().update()
        
        if not self.enabled:
            return
        
        if self.blockcollided.x:
            self.direction = -self.direction
            self.set_speed()
        
        self.animation.update()
    
    def hit_actor(self, actor):
        if isinstance(actor, Player):
            if actor.is_stomping(self):
                self.kill()
                actor.bounce()
            else:
                actor.hurt()
