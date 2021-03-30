class Animation:
    def __init__(self, sprite, game, img_seq=None, delay=None):
        self.sprite = sprite
        self.game = game
        
        self.img_seq = img_seq
        self.delay = delay
        
        self.seq = []
        for image in (self.img_seq or self.sprite.ANIM_IMG_SEQ):
            self.seq.append(self.game.SPRITE_IMAGES[image])
        self.frame = 0
    
    def get_image(self, frame=None):
        return self.seq[frame or self.frame]
    
    def update(self, always_set=False):
        if self.game.frame % (self.delay or self.sprite.ANIM_DELAY) == 0:
            self.frame = (self.frame + 1) % len(self.seq)
            self.sprite.image = self.get_image()
            return True
        
        if always_set:
            self.sprite.image = self.get_image()
        return False
