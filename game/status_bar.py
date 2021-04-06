import pygame
from game import colour

class StatusBar:
    COLOUR = (203, 192, 255)
    
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
        pygame.draw.rect(surface, self.COLOUR, self.rect)
        
        images = []
        
        text, rect = self.game.render_text(f"Lives: {self.game.player.lives}", *self.TEXT_SETTINGS)
        rect.midleft = self.text_rect.midleft
        images.append((text, rect))
        
        heart_image = self.game.IMAGES["heart"]
        empty_heart_image = self.game.IMAGES["empty_heart"]
        heart_rect = heart_image.get_rect()
        health_width = self.game.player.START_HEALTH * heart_rect.width
        for heart in range(self.game.player.START_HEALTH):
            rect = pygame.Rect(heart_rect)
            rect.x = ((self.text_rect.centerx - (health_width / 2))
                + ((heart / self.game.player.START_HEALTH) * health_width))
            rect.centery = self.text_rect.centery
            
            has_heart = heart < self.game.player.health
            images.append((heart_image if has_heart else empty_heart_image, rect))
        
        text, rect = self.game.render_text(f"Coins: {self.game.player.coins}", *self.TEXT_SETTINGS)
        rect.midright = self.text_rect.midright
        images.append((text, rect))
        
        surface.blits(images, False)
        
        
