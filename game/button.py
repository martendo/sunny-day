import pygame

class Button:
    COLOUR = pygame.Color(0, 0, 0, 16)
    HOVER_COLOUR = pygame.Color(0, 0, 0, 32)
    
    def __init__(self, game, rect, button_colour, hover_colour, text, text_colour, func, *func_args):
        self.game = game
        
        self.enabled = False
        
        self.rect = pygame.Rect(rect)
        self.colour = button_colour
        self.hover_colour = hover_colour
        self.text_colour = text_colour
        
        self.text, self.text_rect = self.game.render_text(text, self.game.FONT, text_colour)
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
        surface.set_alpha(self.hover_colour.a if hovered else self.colour.a)
        surface.fill(self.hover_colour if hovered else self.colour)
        self.game.screen.blit(surface, self.rect)
        self.game.screen.blit(self.text, self.text_rect)
