import pygame

class Camera:
    def __init__(self, game):
        self.game = game
        self.pos = pygame.Vector2(0, 0)
    
    def update(self, follow_rect):
        x = follow_rect.centerx - (self.game.WIDTH_PX / 2)
        if x >= 0 and x + self.game.WIDTH_PX < self.game.map.width * self.game.TILE_SIZE:
            self.pos.x = x
        y = follow_rect.centery - (self.game.HEIGHT_PX / 2)
        if y >= 0 and y + self.game.HEIGHT_PX < self.game.map.height * self.game.TILE_SIZE:
            self.pos.y = y

class CameraAwareLayeredGroup(pygame.sprite.LayeredUpdates):
    def __init__(self, map, *sprites, **kwargs):
        super().__init__(*sprites, **kwargs)
        self.map = map
    
    def draw(self, surface):
        # Modified version of pygame.sprite.Group.draw() to adjust for the camera position
        sprites = self.sprites()
        camera = self.map.camera.pos
        if hasattr(surface, "blits"):
            self.spritedict.update(
                zip(
                    sprites,
                    surface.blits((spr.image, spr.rect.move(-camera)) for spr in sprites)
                )
            )
        else:
            for spr in sprites:
                self.spritedict[spr] = surface.blit(spr.image, spr.rect.move(-camera))
        self.lostsprites = []
