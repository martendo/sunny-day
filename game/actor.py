import pygame
from game import block

class Actor(pygame.sprite.Sprite):
    def __init__(self, game, pos, hitbox):
        super().__init__()
        
        self.game = game
        
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(0, 0)
        
        self.hitbox = hitbox
        
        self.game.actors.add(self)
    
    def update(self):
        # Update position
        
        self.pos += self.vel
        
        self.rect.x = int(self.pos.x)
        
        # X-axis collision
        blk = pygame.sprite.spritecollideany(self, self.game.map.blocks, self.hitboxblockcollide)
        if blk is not None:
            if self.vel.x > 0:
                self.pos.x = blk.rect.left - self.hitbox.right
            elif self.vel.x < 0:
                self.pos.x = blk.rect.right - self.hitbox.left
            
            self.rect.x = int(self.pos.x)
            self.vel.x = 0
        
        self.rect.y = int(self.pos.y)
        
        # Y-axis collision
        blk = pygame.sprite.spritecollideany(self, self.game.map.blocks, self.hitboxblockcollide)
        if blk is not None:
            if self.vel.y > 0:
                self.pos.y = blk.rect.top - self.hitbox.bottom
            elif self.vel.y < 0:
                self.pos.y = blk.rect.bottom - self.hitbox.top
            
            self.rect.y = int(self.pos.y)
            self.vel.y = 0
    
    def hitboxblockcollide(self, actor, blk):
        if type(blk) not in block.TYPES[block.SOLIDS_START:]:
            return False
        hitbox = pygame.Rect((actor.rect.x + actor.hitbox.x, actor.rect.y + actor.hitbox.y), actor.hitbox.size)
        return hitbox.colliderect(blk.rect)
