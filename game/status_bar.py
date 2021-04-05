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
        
        self.TEXT_SETTINGS = (self.game.MENU_FONT, colour.BLACK)
    
    def draw(self, surface):
        pygame.draw.rect(surface, colour.STATUS_BAR_COLOUR, self.rect)
        
        texts = []
        
        text, rect = self.game.render_text(f"Coins: {self.game.coins}", *self.TEXT_SETTINGS)
        rect.midleft = self.text_rect.midleft
        texts.append((text, rect))
        
        text, rect = self.game.render_text(f"Lives: {self.game.player.lives}", *self.TEXT_SETTINGS)
        rect.center = self.text_rect.center
        texts.append((text, rect))
        
        text, rect = self.game.render_text(f"Health: {self.game.player.health}", *self.TEXT_SETTINGS)
        rect.midright = self.text_rect.midright
        texts.append((text, rect))
        
        surface.blits(texts, False)
