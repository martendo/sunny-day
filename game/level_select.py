import pygame
from game.button import Button
from game import colour
from game.game_state import GameState

class LevelSelect:
    BUTTON_SIZE = 75
    
    BUTTON_SPOTS = (
        (180, 180),
    )
    
    def __init__(self, game):
        self.game = game
        
        self.BG_IMAGE = self.game.IMAGES["level_select_bg"]
        self.BG_IMAGE_RECT = self.BG_IMAGE.get_rect()
        self.BG_IMAGE_RECT.top = self.game.status_bar.rect.bottom
        
        self.buttons = set()
        for i, spot in enumerate(self.BUTTON_SPOTS):
            num = i + 1
            rect = pygame.Rect((0, 0), (self.BUTTON_SIZE, self.BUTTON_SIZE))
            rect.center = spot
            rect.y += self.game.status_bar.rect.height
            self.buttons.add(Button(
                self.game,
                rect,
                Button.COLOUR,
                Button.HOVER_COLOUR,
                str(num),
                colour.BLACK,
                self.click_level,
                num,
            ))
    
    def init(self):
        self.game.state = GameState.LEVEL_SELECT
    
    def click_level(self, num):
        self.game.screen_fader.start(**{
            "mid_func": self.start_level,
            "mid_func_args": (num,),
        })
    def start_level(self, num):
        self.game.map.load(num)
        self.game.state = GameState.IN_LEVEL
    
    def draw(self, surface):
        surface.blit(self.BG_IMAGE, self.BG_IMAGE_RECT)
        
        for button in self.buttons:
            button.draw()
