import pygame
from game import block

class Actor(pygame.sprite.Sprite):
    def __init__(self, game, pos, hitbox):
        super().__init__()
        
        self.game = game
        
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(0, 0)
        
        self.set_hitbox(hitbox)
        
        self.game.actors.add(self)
    
    def update(self):
        # Update position
        
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
        
        self.rect.x = int(self.pos.x) * self.game.PX_SIZE
        
        # TODO: Fix collision so that actors are pushed to the side
        # of the block they were on and not based on their velocity
        
        # X-axis collision
        blk = pygame.sprite.spritecollideany(self, self.game.map.blocks, self.hitboxblockcollide)
        if blk != None:
            if self.vel.x > 0:
                self.pos.x = (blk.rect.left - self.hitbox.right) // self.game.PX_SIZE
            elif self.vel.x < 0:
                self.pos.x = (blk.rect.right - self.hitbox.left) // self.game.PX_SIZE
            
            self.rect.x = int(self.pos.x) * self.game.PX_SIZE
            self.vel.x = 0
        
        self.rect.y = int(self.pos.y) * self.game.PX_SIZE
        
        # Y-axis collision
        blk = pygame.sprite.spritecollideany(self, self.game.map.blocks, self.hitboxblockcollide)
        if blk != None:
            if self.vel.y > 0:
                self.pos.y = (blk.rect.top - self.hitbox.bottom) // self.game.PX_SIZE
            elif self.vel.y < 0:
                self.pos.y = (blk.rect.bottom - self.hitbox.top) // self.game.PX_SIZE
            
            self.rect.y = int(self.pos.y) * self.game.PX_SIZE
            self.vel.y = 0
    
    def set_hitbox(self, hitbox):
        self.hitbox = pygame.Rect(*map(lambda x: x * self.game.PX_SIZE, hitbox))
    
    def hitboxblockcollide(self, actor, blk):
        if type(blk) not in block.TYPES[block.SOLIDS_START:]:
            return False
        hitbox = pygame.Rect((actor.rect.x + actor.hitbox.x, actor.rect.y + actor.hitbox.y), actor.hitbox.size)
        return hitbox.colliderect(blk.rect)
