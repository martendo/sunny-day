import pygame
from game import colour

class Button:
    COLOUR = pygame.Color(0, 0, 0, 16)
    HOVER_COLOUR = pygame.Color(0, 0, 0, 32)
    TEXT_COLOUR = colour.BLACK
    
    def __init__(self, game, rect, text, func, *func_args):
        self.game = game
        
        self.enabled = False
        
        self.rect = pygame.Rect(rect)
        self.text, self.text_rect = self.game.render_text(text, self.game.FONT, self.TEXT_COLOUR)
        self.text_rect.center = self.rect.center
        self.surface = pygame.Surface(self.rect.size)
        
        self.func = func
        self.func_args = func_args
        
        self.game.buttons.add(self)
    
    def is_hovered(self, mouse):
        return (self.rect.left < mouse[0] < self.rect.right
            and self.rect.top < mouse[1] < self.rect.bottom)
    
    def click(self):
        self.func(*self.func_args)
    
    def draw(self, surface):
        hovered = self.is_hovered(pygame.mouse.get_pos())
        
        self.surface.set_alpha(self.HOVER_COLOUR.a if hovered else self.COLOUR.a)
        self.surface.fill(self.HOVER_COLOUR if hovered else self.COLOUR)
        surface.blit(self.surface, self.rect)
        surface.blit(self.text, self.text_rect)

class LevelButton(Button):
    LOCKED = 0
    COMPLETED = 1
    NEW = 2
    
    COLOURS = {
        LOCKED: {
            "normal": (152, 152, 152),
        },
        COMPLETED: {
            "normal": (126, 255, 74),
            "hover": (106, 217, 61),
        },
        NEW: {
            "normal": (255, 90, 90),
            "hover": (205, 76, 76),
        },
    }
    BORDER_COLOUR = colour.BLACK
    BORDER_WIDTH = 5
    
    def __init__(self, status, *args):
        super().__init__(*args)
        
        self.status = status
        
    def draw(self, surface):
        hovered = self.is_hovered(pygame.mouse.get_pos())
        colour = self.COLOURS[self.status]["hover" if (hovered
            and self.status != self.LOCKED) else "normal"]
        pygame.draw.rect(surface, colour, self.rect)
        pygame.draw.rect(surface, self.BORDER_COLOUR, self.rect, self.BORDER_WIDTH)
        surface.blit(self.text, self.text_rect)
