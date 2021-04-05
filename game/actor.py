import pygame

class Actor(pygame.sprite.Sprite):
    def __init__(self, game, hitbox, pos=None):
        super().__init__()
        
        self.game = game
        
        self.pos = pygame.Vector2(pos or (0, 0))
        self.vel = pygame.Vector2(0, 0)
        self.direction = self.game.DIR_LEFT
        
        self.hitbox = hitbox
        self.blockcollided = [False, False]
        
        self.game.actors.add(self)
    
    def set_rect(self, rect):
        self.rect = rect
        self.rect.left = int(self.pos.x)
        self.rect.bottom = int(self.pos.y)
    
    def update(self):
        self.pos += self.vel
        
        self.blockcollided = [False, False]
        
        self.rect.left = int(self.pos.x)
        # x-axis collision
        block = self.block_colliding("x")
        if block is not None:
            if self.vel.x > 0:
                self.pos.x = block.rect.left - self.hitbox.right
            elif self.vel.x < 0:
                self.pos.x = block.rect.right - self.hitbox.left
            self.collided_x()
        
        # End of map
        map_width_px = self.game.map.width * self.game.TILE_SIZE
        if self.rect.x + self.hitbox.left < 0:
            self.pos.x = 0 - self.hitbox.left
            self.collided_x()
        elif self.rect.x + self.hitbox.right > map_width_px:
            self.pos.x = map_width_px - self.hitbox.right
            self.collided_x()
        
        self.rect.bottom = int(self.pos.y)
        # y-axis collision
        block = self.block_colliding("y")
        if block is not None:
            if self.vel.y > 0:
                self.pos.y = block.rect.top + (self.rect.height - self.hitbox.bottom)
            elif self.vel.y < 0:
                self.pos.y = block.rect.bottom + (self.rect.height - self.hitbox.top)
            self.collided_y()
        
        if self.rect.top // self.game.TILE_SIZE > self.game.map.height:
            self.die()
    
    def block_colliding(self, axis):
        hitbox = pygame.Rect((self.rect.x + self.hitbox.x, self.rect.y + self.hitbox.y), self.hitbox.size)
        for y in range(hitbox.top, hitbox.bottom):
            for x in range(hitbox.left, hitbox.right):
                tile_x = x // self.game.TILE_SIZE
                tile_y = y // self.game.TILE_SIZE
                block = self.game.map.get_block(tile_x, tile_y)
                if block.is_solid:
                    return block
                elif (block.is_one_way and axis == "y"
                        and self.vel.y > 0
                        and (self.rect.y + self.hitbox.bottom
                            <= block.rect.top + self.game.COLLISION_OFFSET)):
                    return block
        return None
    
    def collided_x(self):
        self.blockcollided[0] = True
        self.rect.left = int(self.pos.x)
        self.vel.x = 0
    def collided_y(self):
        self.blockcollided[1] = True
        self.rect.bottom = int(self.pos.y)
        self.vel.y = 0
    
    def die(self):
        self.kill()
