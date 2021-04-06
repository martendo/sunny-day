from game.button import Button
from game import colour
from game.game_state import GameState

class LevelSelect:
    BUTTON_SIZE = 75
    SPACING = 50
    
    def __init__(self, game):
        self.game = game
        
        self.buttons = set()
        
        for i in range(self.game.LEVEL_COUNT):
            num = i + 1
            
            self.buttons.add(Button(
                self.game,
                (
                    self.SPACING + (self.BUTTON_SIZE + self.SPACING) * i,
                    # TODO: Decide on rows of buttons when there are more levels
                    self.SPACING,
                    self.BUTTON_SIZE,
                    self.BUTTON_SIZE,
                ),
                Button.COLOUR,
                Button.HOVER_COLOUR,
                str(num),
                colour.BLACK,
                self.start_level,
                num,
            ))
    
    def init(self):
        self.game.state = GameState.LEVEL_SELECT
    
    def start_level(self, num):
        self.game.map.load(num)
        self.game.state = GameState.IN_LEVEL
    
    def draw(self, surface):
        surface.fill(colour.PLACEHOLDER)
        
        for button in self.buttons:
            button.draw()
