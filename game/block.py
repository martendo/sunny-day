import pygame

class Block(pygame.sprite.Sprite):
    ONE_WAY = 3
    SOLIDS_START = 4
    
    def __init__(self, game, x, y, tile_id, flip):
        super().__init__()
        
        self.game = game
        
        self.tile_id = tile_id
        self.is_solid = self.tile_id >= self.SOLIDS_START
        self.is_one_way = self.tile_id == self.ONE_WAY
        
        self.image = self.game.TILESET[self.tile_id]
        self.flip = flip
        if self.flip["d"]:
            self.image = pygame.transform.flip(pygame.transform.rotate(self.image, 270), True, False)
        if self.flip["h"] or self.flip["v"]:
            self.image = pygame.transform.flip(self.image, self.flip["h"], self.flip["v"])
        
        self.rect = self.image.get_rect()
        self.rect.x = x * self.game.TILE_SIZE
        self.rect.y = y * self.game.TILE_SIZE
