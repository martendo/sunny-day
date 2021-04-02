class Animation:
    def __init__(self, sprite, game, settings):
        self.sprite = sprite
        self.game = game
        
        self.settings = settings
        
        self.seq = []
        for image in self.settings["img"]:
            self.seq.append(self.game.SPRITE_IMAGES[image])
        self.lengths = self.settings["lengths"]
        self.frame = 0
        self.delay = self._get_delay()
    
    def get_image(self, frame=None):
        return self.seq[frame or self.frame]
    
    def _get_delay(self):
        return self.lengths if isinstance(self.lengths, int) else self.lengths[self.frame]
    
    def update(self, always_set=False):
        if self.game.frame % self.delay == 0:
            self.frame = (self.frame + 1) % len(self.seq)
            self.delay = self._get_delay()
            self.sprite.image = self.get_image()
            return True
        
        if always_set:
            self.sprite.image = self.get_image()
        return False
