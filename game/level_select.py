import pygame
from game.button import Button
from game import colour
from game.game_state import GameState

class LevelSelect:
    BUTTON_SIZE = 75
    BUTTON_SPOTS = (
        (180, 180),
    )
    
    LOCKED_COLOUR = pygame.Color(152, 152, 152, 64)
    COMPLETED_COLOUR = pygame.Color(126, 255, 74, 64)
    NEW_COLOUR = pygame.Color(255, 90, 90, 64)
    HOVER_ALPHA = 128
    
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
                cur_colour = self.COMPLETED_COLOUR
            elif self.game.last_completed_level + 1 < num:
                cur_colour = self.LOCKED_COLOUR
            else:
                cur_colour = self.NEW_COLOUR
            
            if self.game.last_completed_level + 1 >= num:
                hover_colour = pygame.Color(cur_colour)
                hover_colour.a = self.HOVER_ALPHA
            else:
                hover_colour = cur_colour
            
            self.buttons.add(Button(
                self.game,
                rect,
                cur_colour,
                hover_colour,
                str(num),
                colour.BLACK,
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
            button.draw()
