import pygame
from game.animation import Animation
from game import colour

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        
        self.game = game
        
        self.image = pygame.Surface((self.game.TILE_SIZE, self.game.TILE_SIZE))
        self.image.fill(colour.PLACEHOLDER)
        self.rect = self.image.get_rect()
        self.rect.x = x * self.game.TILE_SIZE
        self.rect.y = y * self.game.TILE_SIZE

class Sky(Block):
    IMAGE = "sky"
    
    def __init__(self, *args):
        super().__init__(*args)
        
        self.image = self.game.IMAGES[self.IMAGE]

class Flower(Block):
    ANIM_IMG_SEQ = (
        "flower-1",
        "flower-2",
        "flower-3",
        "flower-2",
    )
    ANIM_DELAY = 16
    
    def __init__(self, *args):
        super().__init__(*args)
        
        self.animation = Animation(self, self.game)
        self.image = self.animation.get_image()
    
    def update(self):
        self.animation.update()

class Grass(Block):
    IMAGE = "grass"
    
    def __init__(self, *args):
        super().__init__(*args)
        
        self.image = self.game.IMAGES[self.IMAGE]

class Brick(Block):
    IMAGE = "brick"
    
    def __init__(self, *args):
        super().__init__(*args)
        
        self.image = self.game.IMAGES[self.IMAGE]

TYPES = (
    # Non-solid
    Sky,
    Flower,
    
    # Solid
    Grass,
    Brick,
)
SOLIDS_START = 2
