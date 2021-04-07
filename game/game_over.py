from game.game_state import GameState
from game import colour

class GameOver:
    BG_COLOUR = colour.BLACK
    TEXT_COLOUR = colour.WHITE
    
    def __init__(self, game):
        self.game = game
        
        self.text, self.text_rect = self.game.render_text(
            "GAME OVER!",
            self.game.FONT,
            self.TEXT_COLOUR,
            self.BG_COLOUR
        )
        self.text_rect.center = (self.game.WIDTH / 2, self.game.HEIGHT / 2)
    
    def show(self):
        self.game.state = GameState.GAME_OVER
    def hide(self):
        self.game.state = GameState.LEVEL_SELECT
    
    def draw(self, surface):
        surface.fill(self.BG_COLOUR)
        surface.blit(self.text, self.text_rect)
