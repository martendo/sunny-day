import pygame
from game import colour

class Button:
    def __init__(self, game, rect, button_colour, hover_colour, text, text_colour, func, *func_args):
        self.game = game
        
        self.rect = pygame.Rect(rect)
        self.colour = button_colour
        self.hover_colour = hover_colour
        self.text_colour = text_colour
        
        self.text, self.text_rect = self.game.render_text(text, text_colour)
        self.text_rect.center = self.rect.center
        
        self.func = func
        self.func_args = func_args
        
        self.game.buttons.add(self)
    
    def is_hovered(self, mouse):
        return (self.rect.left < mouse[0] < self.rect.right
            and self.rect.top < mouse[1] < self.rect.bottom)
    
    def click(self):
        self.func(*self.func_args)
    
    def draw(self):
        hovered = self.is_hovered(pygame.mouse.get_pos())
        
        surface = pygame.Surface(self.rect.size)
        surface.set_alpha(colour.BUTTON_HOVER.a if hovered else colour.BUTTON_COLOUR.a)
        surface.fill(self.hover_colour if hovered else self.colour)
        self.game.screen.blit(surface, self.rect)
        self.game.screen.blit(self.text, self.text_rect)