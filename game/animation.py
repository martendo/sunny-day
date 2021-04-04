import pygame
from game.actor import Actor
from game.block import Block

class Animation:
    def __init__(self, sprite, game, settings):
        self.sprite = sprite
        self.game = game
        
        self.settings = settings
        
        image_source = (self.game.TILESET if isinstance(sprite, Block)
            else self.game.ACTOR_IMAGES)
        self.seq = []
        for image in self.settings["img"]:
            self.seq.append(image_source[image])
        self.lengths = self.settings["lengths"]
        
        self.frame = 0
        self._update_frame_length()
    
    def get_image(self, frame=None):
        return self.seq[frame or self.frame]
    
    def set_image(self, frame=None, image=None):
        self.sprite.image = image or self.get_image(frame)
        if isinstance(self.sprite, Actor) and self.sprite.direction == self.game.DIR_RIGHT:
            # All images are left-facing
            self.sprite.image = pygame.transform.flip(self.sprite.image, True, False)
    
    def set_frame_length(self, length):
        self.delay = length
        self.countdown = self.delay
    
    def _update_frame_length(self):
        self.set_frame_length(self.lengths if isinstance(self.lengths, int) else self.lengths[self.frame])
    
    def update(self, always_set=False):
        self.countdown -= 1
        if self.countdown == 0:
            self.frame = (self.frame + 1) % len(self.seq)
            self._update_frame_length()
            self.set_image()
            return True
        if always_set:
            self.set_image()
        return False
