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
        self.sun_angle = 0
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
    
    def click_start(self):
        self.game.screen_fader.start(mid_func=self.start_game)
    def show(self):
        self.game.state = GameState.TITLE_SCREEN
        self.START_BUTTON.enabled = True
    def start_game(self):
        self.game.FILE_SELECT.show()
        self.START_BUTTON.enabled = False
    
    def update(self):
        self.sun_angle += self.SUN_ROTATION
    
    def draw(self, surface):
        # Rotate sun
        image = pygame.transform.rotate(self.SUN, self.sun_angle)
        rect = image.get_rect()
        rect.center = (self.game.WIDTH - self.SPACING, self.SPACING)
        
        surface.blits(((self.BG, self.BG_RECT), (image, rect)), False)
        
        self.START_BUTTON.draw(surface)
