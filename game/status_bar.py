import pygame
from game import colour

class StatusBar:
    def __init__(self, game):
        self.game = game
        
        self.rect = pygame.Rect(0, 0,
            self.game.WIDTH, self.game.MENU_FONT_SIZE * 3)
        self.text_rect = pygame.Rect(
            self.rect.x + self.game.MENU_FONT_SIZE,
            self.rect.y + self.game.MENU_FONT_SIZE,
            self.rect.width - self.game.MENU_FONT_SIZE * 2,
            self.game.MENU_FONT_SIZE,
        )
    
    def draw(self, surface):
        pygame.draw.rect(surface, colour.STATUS_BAR_COLOUR, self.rect)
        
        text, rect = self.game.render_text(f"Coins: {self.game.coins}", self.game.MENU_FONT, colour.BLACK)
        rect.midleft = self.text_rect.midleft
        surface.blit(text, rect)
