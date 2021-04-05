import pygame
from game.animation import Animation

class Block(pygame.sprite.Sprite):
    ONE_WAY = 3
    SOLIDS_START = 4
    
    def __init__(self, game, gamemap, x, y, tile_id, flip):
        super().__init__()
        
        self.game = game
        self.map = gamemap
        
        self.tile_id = tile_id
        self.is_solid = self.tile_id >= self.SOLIDS_START
        self.is_one_way = self.tile_id == self.ONE_WAY
        
        self.animation = None
        for tile in self.map.tileset["tiles"]:
            if tile["id"] != self.tile_id:
                continue
            
            # Tile has an animation
            if "animation" in tile:
                self.animation = Animation(self, self.game, {
                    "img": tuple(map(lambda frame: frame["tileid"], tile["animation"])),
                    "duration": tuple(map(lambda frame: frame["duration"], tile["animation"])),
                })
            break
        self.image = self.game.TILESET[self.tile_id]
        self.flip_image(flip)
        
        self.rect = self.image.get_rect()
        self.rect.x = x * self.game.TILE_SIZE
        self.rect.y = y * self.game.TILE_SIZE
    
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
