import pygame
from game.animation import Animation

class Block(pygame.sprite.Sprite):
    COIN = 3
    ONE_WAY = 6
    SOLIDS_START = 7
    
    def __init__(self, game, gamemap, x, y, tile_id, flip):
        super().__init__()
        
        self.game = game
        self.map = gamemap
        
        self.tile_id = tile_id
        self.is_coin = self.tile_id == self.COIN
        self.is_solid = self.tile_id >= self.SOLIDS_START
        self.is_one_way = self.tile_id == self.ONE_WAY
        
        self.animation = None
        tile = self.map.get_tile(self.tile_id)
        if tile is not None and "animation" in tile:
            # Tile has an animation
            self.animation = Animation(self, self.game, {
                "img": tuple(map(lambda frame: frame["tileid"], tile["animation"])),
                "duration": tuple(map(lambda frame: frame["duration"], tile["animation"])),
            })
        self.image = self.game.TILESET[self.tile_id]
        self.flip_image(flip)
        
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.x = self.x * self.game.TILE_SIZE
        self.rect.y = self.y * self.game.TILE_SIZE
    
    def flip_image(self, flip=None):
        if flip is not None:
            self.flip = flip
        
        if self.flip["d"]:
            self.image = pygame.transform.rotate(pygame.transform.flip(self.image, True, False), 90)
        if self.flip["h"] or self.flip["v"]:
            self.image = pygame.transform.flip(self.image, self.flip["h"], self.flip["v"])
    
    def update(self):
        if self.animation is not None:
            if self.animation.update():
                self.flip_image()
