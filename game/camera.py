import pygame

class CameraAwareGroup(pygame.sprite.Group):
    def __init__(self, map, *sprites):
        super().__init__(*sprites)
        self.map = map
    
    def draw(self, surface):
        # Modified version of pygame.sprite.Group.draw() to adjust for the camera position
        sprites = self.sprites()
        camera = self.map.camera
        if hasattr(surface, "blits"):
            self.spritedict.update(
                zip(
                    sprites,
                    surface.blits((spr.image, spr.rect.move(camera)) for spr in sprites)
                )
            )
        else:
            for spr in sprites:
                self.spritedict[spr] = surface.blit(spr.image, spr.rect.move(camera))
        self.lostsprites = []
