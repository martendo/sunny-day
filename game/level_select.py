import pygame
from game.button import LevelButton
from game.game_state import GameState

class LevelSelect:
    BUTTON_SIZE = 75
    BUTTON_SPOTS = (
        (180, 180),
        (750, 200),
    )
    
    def __init__(self, game):
        self.game = game
        
        self.BG_IMAGE = self.game.IMAGES["level_select_bg"]
        self.BG_IMAGE_RECT = self.BG_IMAGE.get_rect()
        self.BG_IMAGE_RECT.top = self.game.status_bar.rect.bottom
        
        self.buttons = set()
    
    def make_buttons(self):
        self.game.buttons -= self.buttons
        self.buttons.clear()
        for i, spot in enumerate(self.BUTTON_SPOTS):
            num = i + 1
            
            rect = pygame.Rect((0, 0), (self.BUTTON_SIZE, self.BUTTON_SIZE))
            rect.center = spot
            rect.y += self.game.status_bar.rect.height
            
            if self.game.last_completed_level + 1 > num:
                state = LevelButton.COMPLETED
            elif self.game.last_completed_level + 1 < num:
                state = LevelButton.LOCKED
            else:
                state = LevelButton.NEW
            
            self.buttons.add(LevelButton(
                state,
                self.game,
                rect,
                str(num),
                self.click_level,
                num,
            ))
    
    def click_level(self, num):
        if num > self.game.last_completed_level + 1:
            # Locked
            return
        self.game.screen_fader.start(
            mid_func=self.start_level,
            mid_func_args=(num,),
        )
    def show(self):
        self.game.state = GameState.LEVEL_SELECT
        self.make_buttons()
        for button in self.buttons:
            button.enabled = True
    def start_level(self, num):
        self.game.map.load(num)
        self.game.state = GameState.IN_LEVEL
        self.game.buttons -= self.buttons
    
    def draw(self, surface):
        surface.blit(self.BG_IMAGE, self.BG_IMAGE_RECT)
        
        for button in self.buttons:
            button.draw(surface)
