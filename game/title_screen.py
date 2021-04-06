import pygame
from game.button import Button
from game import colour
from game.game_state import GameState

class TitleScreen:
    SPACING = 30
    NAME_RECT = pygame.Rect(SPACING, SPACING, 600, 400)
    BUTTON_HEIGHT = 100
    
    SUN_ROTATION = 0.25
    
    def __init__(self, game):
        self.game = game
        
        self.BG = self.game.IMAGES["title"]
        self.BG_RECT = self.BG.get_rect()
        
        self.SUN = self.game.IMAGES["title_sun"]
        # Sun changes - handle that in draw()
        
        self.START_BUTTON = Button(
            self.game,
            (
                self.SPACING,
                self.NAME_RECT.bottom + self.SPACING,
                self.NAME_RECT.width,
                self.BUTTON_HEIGHT
            ),
            Button.COLOUR,
            Button.HOVER_COLOUR,
            "Play!",
            colour.BLACK,
            self.click_start,
        )
        
        self.init()
    
    def init(self):
        self.game.state = GameState.TITLE_SCREEN
        self.sun_angle = 0
    
    def click_start(self):
        self.game.screen_fader.start(**{
            "end_func": self.start_game,
        })
    def start_game(self):
        self.game.state = GameState.LEVEL_SELECT
    
    def update(self):
        self.sun_angle += self.SUN_ROTATION
    
    def draw(self, surface, allow_fade=True):
        if not self.game.screen_fader.midway or not allow_fade:
            # Rotate sun
            image = pygame.transform.rotate(self.SUN, self.sun_angle)
            rect = image.get_rect()
            rect.center = (self.game.WIDTH - self.SPACING, self.SPACING)
            
            surface.blits(((self.BG, self.BG_RECT), (image, rect)), False)
            
            self.START_BUTTON.draw()
        else:
            self.game.LEVEL_SELECT.draw(surface, allow_fade=False)
        
        if self.game.screen_fader.fading:
            self.game.screen_fader.update(surface)
