import pygame
from time import time
from game import colour

class ScreenFader:
    DEFAULT_COLOUR = colour.BLACK
    DEFAULT_DURATION = 0.75
    
    def __init__(self, game):
        self.game = game
        self.surface = pygame.Surface(self.game.screen.get_size())
        self.rect = self.surface.get_rect()
        self.fading = False
        self.midway = False
    
    def start(self, mid_func=None, mid_func_args=(),
            end_func=None, end_func_args=(), colour=None, duration=None):
        self.surface.fill(colour if colour is not None else self.DEFAULT_COLOUR)
        self.duration = duration if duration is not None else self.DEFAULT_DURATION
        
        self.mid_func = mid_func
        self.mid_func_args = mid_func_args
        self.midway = False
        self.end_func = end_func
        self.end_func_args = end_func_args
        
        self.start_time = time()
        self.fading = True
    
    def update(self, surface):
        if time() >= self.start_time + self.duration:
            self.fading = False
            self.midway = False
            if self.end_func is not None:
                self.end_func(*self.end_func_args)
            return
        
        alpha = ((time() - self.start_time) / (self.duration / 2)) * 255
        if alpha > 255:
            alpha -= (alpha % 255) * 2
            if not self.midway:
                self.midway = True
                if self.mid_func is not None:
                    self.mid_func(*self.mid_func_args)
        
        self.surface.set_alpha(alpha)
        surface.blit(self.surface, self.rect)
