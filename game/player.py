import pygame
from game.actor import Actor
from game.animation import Animation

class Player(Actor):
    ACCEL = 0.5
    CROUCH_SPEED = 0.5
    FRICTION = 1/3
    MAX_WALK_VELX = 2
    MAX_RUN_VELX = 4
    MAX_VELY = 10
    
    # Small jump: 2 blocks high
    JUMP_VEL = -4
    # High jump: 3 blocks high
    HIGH_JUMP = 0.2
    # Crouch-jump: 1 block high
    CROUCH_JUMP_VEL = -3.1
    
    # Normal hitbox
    HITBOX = (
        4, 1,
        8, 15,
    )
    # Smaller crouching hitbox
    CROUCH_HITBOX = (
        4, 8,
        8, 8,
    )
    
    IDLE_ANIM_IMG_SEQ = (
        "player-1",
        "player-1",
        "player-1",
        "player-1",
        "player-2",
        "player-3",
        "player-3",
        "player-3",
        "player-3",
        "player-2",
    )
    IDLE_ANIM_DELAY = 3
    
    MOVING_ANIM_IMG_SEQ = (
        "player-m-1",
        "player-m-2",
        "player-m-3",
        "player-m-4",
        "player-m-5",
    )
    MOVING_ANIM_DELAY = 2
    
    CROUCH_IDLE_ANIM_IMG_SEQ = (
        "player-c-1",
        "player-c-2",
    )
    CROUCH_IDLE_ANIM_DELAY = 16
    
    def __init__(self, *args):
        super().__init__(*args, self.HITBOX)
        
        self.IDLE_ANIMATION = Animation(self, self.game, self.IDLE_ANIM_IMG_SEQ, self.IDLE_ANIM_DELAY)
        self.MOVING_ANIMATION = Animation(self, self.game, self.MOVING_ANIM_IMG_SEQ, self.MOVING_ANIM_DELAY)
        self.CROUCH_IDLE_ANIMATION = Animation(self, self.game, self.CROUCH_IDLE_ANIM_IMG_SEQ, self.CROUCH_IDLE_ANIM_DELAY)
        
        self.animation = self.IDLE_ANIMATION
        self.image = self.animation.get_image()
        self.rect = self.image.get_rect()
        
        self.direction = self.game.DIR_LEFT
        
        self.running = False
        self.crouching = False
        self.jumping = False
    
    def update(self):
        pressed = pygame.key.get_pressed()
        
        moving = False
        # Horizontal acceleration
        if pressed[self.game.MOVE_RIGHT_KEY]:
            if not self.crouching:
                self.vel.x += self.ACCEL
            elif self.vel.x < self.CROUCH_SPEED:
                self.vel.x = self.CROUCH_SPEED
            moving = True
        if pressed[self.game.MOVE_LEFT_KEY]:
            if not self.crouching:
                self.vel.x -= self.ACCEL
            elif self.vel.x > -self.CROUCH_SPEED:
                self.vel.x = -self.CROUCH_SPEED
            moving = True
        
        # TODO: Player's vel.x is nonzero when moving to the right into
        # a block, causing it to show the moving animation
        
        if not self.crouching or (moving and abs(self.vel.x) > self.CROUCH_SPEED) or (not moving and self.vel.x != 0):
            # Friction
            if self.vel.x > 0:
                self.vel.x -= self.FRICTION
                # Friction should not make you start moving the other way
                if self.vel.x < 0:
                    self.vel.x = 0
            elif self.vel.x < 0:
                self.vel.x += self.FRICTION
                if self.vel.x > 0:
                    self.vel.x = 0
        
        # Holding down the jump key, jump for longer
        if self.jumping and not self.crouching:
            self.vel.y -= self.HIGH_JUMP
        
        # Cap velocity
        MAX_VELX = self.MAX_RUN_VELX if self.running else self.MAX_WALK_VELX
        
        if self.vel.x > MAX_VELX:
            self.vel.x = MAX_VELX
        elif self.vel.x < -MAX_VELX:
            self.vel.x = -MAX_VELX
        
        if self.vel.y > self.MAX_VELY:
            self.vel.y = self.MAX_VELY
        
        super().update()
        
        if self.pos.y // self.game.TILE_PX > self.game.map.height:
            self.game.game_over()
        
        # Save direction so if vel.x == 0 the direction does not change
        if self.vel.x > 0:
            self.direction = self.game.DIR_RIGHT
        elif self.vel.x < 0:
            self.direction = self.game.DIR_LEFT
        
        # Animate!
        if not self.crouching:
            if self.vel.x != 0:
                # Set animation delay based on velocity (1-3 frames delay)
                self.MOVING_ANIMATION.delay = int((self.MAX_RUN_VELX - abs(self.vel.x)) / 2 + 1)
                self.animation = self.MOVING_ANIMATION
            else:
                self.animation = self.IDLE_ANIMATION
        else:
            # TODO: Crouch-walking animation
            self.animation = self.CROUCH_IDLE_ANIMATION
        # TODO: Make jump image/animation
        
        # Always set the player image because the animation may change at any time
        self.animation.update(always_set=True)
        
        if self.direction == self.game.DIR_RIGHT:
            # Images are left-facing
            self.image = pygame.transform.flip(self.image, True, False)
    
    def draw(self):
        self.game.screen.blit(self.image, self.rect)
    
    def start_running(self):
        self.running = True
    def stop_running(self):
        self.running = False
    
    def jump(self):
        if not self.game.can_jump(self):
            return
        self.jumping = True
        if not self.crouching:
            self.vel.y = self.JUMP_VEL
        else:
            self.vel.y = self.CROUCH_JUMP_VEL
    def release_jump(self):
        self.jumping = False
    
    def crouch(self):
        self.crouching = True
        self.set_hitbox(self.CROUCH_HITBOX)
    def uncrouch(self):
        self.crouching = False
        self.set_hitbox(self.HITBOX)
