import pygame
from game import block

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
    
    def update(self):
        self.pos += self.vel
        
        self.blockcollided = [False, False]
        
        self.rect.x = int(self.pos.x)
        # x-axis collision
        blk = pygame.sprite.spritecollideany(self, self.game.map.blocks, self.hitboxblockcollide)
        if blk is not None:
            if self.vel.x > 0:
                self.pos.x = blk.rect.left - self.hitbox.right
            elif self.vel.x < 0:
                self.pos.x = blk.rect.right - self.hitbox.left
            self.collided_x()
        
        # End of map
        map_width_px = self.game.map.width * self.game.TILE_SIZE
        if self.rect.x + self.hitbox.left < 0:
            self.pos.x = 0 - self.hitbox.left
            self.collided_x()
        elif self.rect.x + self.hitbox.right > map_width_px:
            self.pos.x = map_width_px - self.hitbox.right
            self.collided_x()
        
        self.rect.y = int(self.pos.y)
        # y-axis collision
        blk = pygame.sprite.spritecollideany(self, self.game.map.blocks, self.hitboxblockcollide)
        if blk is not None:
            if self.vel.y > 0:
                self.pos.y = blk.rect.top - self.hitbox.bottom
            elif self.vel.y < 0:
                self.pos.y = blk.rect.bottom - self.hitbox.top
            self.collided_y()
        
        if self.pos.y // self.game.TILE_SIZE > self.game.map.height:
            self.die()
    
    def collided_x(self):
        self.blockcollided[0] = True
        self.rect.x = int(self.pos.x)
        self.vel.x = 0
    def collided_y(self):
        self.blockcollided[1] = True
        self.rect.y = int(self.pos.y)
        self.vel.y = 0
    
    def die(self):
        self.kill()
    
    def hitboxblockcollide(self, actor, blk):
        if isinstance(blk, block.TYPES[block.ONE_WAY]):
            if (actor.vel.y < 0 or (actor.rect.y + actor.hitbox.bottom
                    > blk.rect.top + self.game.COLLISION_OFFSET)):
                return False
        elif type(blk) not in block.TYPES[block.SOLIDS_START:]:
            return False
        hitbox = pygame.Rect((actor.rect.x + actor.hitbox.x, actor.rect.y + actor.hitbox.y), actor.hitbox.size)
        return hitbox.colliderect(blk.rect)
