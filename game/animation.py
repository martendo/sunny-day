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
        self._update_frame_length()
    
    def get_image(self, frame=None):
        return self.seq[frame or self.frame]
    
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
            self.sprite.image = self.get_image()
            return True
        if always_set:
            self.sprite.image = self.get_image()
        return False
