import pygame

class Camera:
    def __init__(self, game):
        self.game = game
        self.Y_OFFSET = self.game.HEIGHT_PX / 3
        self.X_OFFSET = self.game.WIDTH_PX / 2
        self.pos = pygame.Vector2(0, 0)
    
    def update(self, follow_rect):
        x = follow_rect.centerx - self.X_OFFSET
        map_width_px = self.game.map.width * self.game.TILE_SIZE
        if x < 0:
            self.pos.x = 0
        elif x + self.game.WIDTH_PX >= map_width_px:
            self.pos.x = map_width_px - self.game.WIDTH_PX
        else:
            self.pos.x = x
        
        y = follow_rect.centery - self.Y_OFFSET
        map_height_px = self.game.map.height * self.game.TILE_SIZE
        if y < 0:
            self.pos.y = 0
        elif y + self.game.HEIGHT_PX >= map_height_px:
            self.pos.y = map_height_px - self.game.HEIGHT_PX
        else:
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
