import pygame
from game.actor import Actor
from game.animation import Animation
from game import block

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
    HITBOX = pygame.Rect(
        4, 1,
        8, 15,
    )
    # Smaller crouching hitbox
    CROUCH_HITBOX = pygame.Rect(
        4, 8,
        8, 8,
    )
    
    IDLE_ANIMATION_SETTINGS = {
        "img": (
            "player-1",
            "player-2",
            "player-3",
            "player-2",
        ),
        "lengths": (
            12,
            3,
            12,
            3,
        ),
    }
    
    MOVING_ANIMATION_SETTINGS = {
        "img": (
            "player-m-1",
            "player-m-2",
            "player-m-3",
            "player-m-4",
            "player-m-5",
        ),
        "lengths": 2,
    }
    
    CROUCH_IDLE_ANIMATION_SETTINGS = {
        "img": (
            "player-c-1",
            "player-c-2",
        ),
        "lengths": 16,
    }
    
    CROUCH_MOVING_ANIMATION_SETTINGS = {
        "img": (
            "player-c-m-1",
            "player-c-1",
            "player-c-m-2",
            "player-c-2",
        ),
        "lengths": (
            6,
            3,
            6,
            3,
        ),
    }
    
    layer = 1
    
    def __init__(self, *args):
        super().__init__(*args, self.HITBOX)
        
        self.IDLE_ANIMATION = Animation(self, self.game, self.IDLE_ANIMATION_SETTINGS)
        self.MOVING_ANIMATION = Animation(self, self.game, self.MOVING_ANIMATION_SETTINGS)
        self.CROUCH_IDLE_ANIMATION = Animation(self, self.game, self.CROUCH_IDLE_ANIMATION_SETTINGS)
        self.CROUCH_MOVING_ANIMATION = Animation(self, self.game, self.CROUCH_MOVING_ANIMATION_SETTINGS)
        
        self.animation = self.IDLE_ANIMATION
        self.image = self.animation.get_image()
        self.rect = self.image.get_rect()
        
        self.direction = self.game.DIR_LEFT
        
        self.moving = False
        self.running = False
        self.crouching = False
        self.jumping = False
        
        self.lives = 5
    
    def update(self):
        on_ground = self.game.on_ground(self)
        
        pressed = pygame.key.get_pressed()
        
        self.moving = False
        # Horizontal acceleration
        if pressed[self.game.MOVE_RIGHT_KEY]:
            if not self.crouching:
                if on_ground:
                    self.vel.x += self.ACCEL
                else:
                    self.vel.x += self.ACCEL / 2
            elif self.vel.x < self.CROUCH_SPEED:
                self.vel.x = self.CROUCH_SPEED
            self.moving = True
        if pressed[self.game.MOVE_LEFT_KEY]:
            if not self.crouching:
                if on_ground:
                    self.vel.x -= self.ACCEL
                else:
                    self.vel.x -= self.ACCEL / 2
            elif self.vel.x > -self.CROUCH_SPEED:
                if self.vel.x == self.CROUCH_SPEED:
                    self.vel.x = 0
                else:
                    self.vel.x = -self.CROUCH_SPEED
            self.moving = True
        
        if self.crouching and not pressed[self.game.CROUCH_KEY]:
            self.uncrouch()
        
        # TODO: Player's vel.x is nonzero when moving to the right into
        # a block, causing it to show the moving animation
        
        if (not self.crouching
                or (self.crouching and self.moving and abs(self.vel.x) > self.CROUCH_SPEED)
                or (self.crouching and not self.moving)):
            # Friction
            if self.vel.x > 0:
                if on_ground:
                    self.vel.x -= self.FRICTION
                else:
                    self.vel.x -= self.FRICTION / 2
                
                # Friction should not make you start moving the other way
                if self.vel.x < 0:
                    self.vel.x = 0
            elif self.vel.x < 0:
                if on_ground:
                    self.vel.x += self.FRICTION
                else:
                    self.vel.x += self.FRICTION / 2
                
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
        
        if self.pos.y // self.game.TILE_SIZE > self.game.map.height:
            self.die()
        
        # Save direction so if vel.x == 0 the direction does not change
        if self.vel.x > 0:
            self.direction = self.game.DIR_RIGHT
        elif self.vel.x < 0:
            self.direction = self.game.DIR_LEFT
        
        # Animate!
        if not self.crouching:
            if self.vel.x != 0:
                # Set animation delay based on velocity (1-3 frames delay)
                delay = int((self.MAX_RUN_VELX - abs(self.vel.x)) / 2 + 1)
                if self.MOVING_ANIMATION.delay > delay:
                    self.MOVING_ANIMATION.set_frame_length(delay)
                self.animation = self.MOVING_ANIMATION
            else:
                self.animation = self.IDLE_ANIMATION
        else:
            if self.moving and self.vel.x != 0:
                self.animation = self.CROUCH_MOVING_ANIMATION
            else:
                self.animation = self.CROUCH_IDLE_ANIMATION
        # TODO: Make jump image/animation
        
        # Always set the player image because the animation may change at any time
        self.animation.update(always_set=True)
        
        if self.direction == self.game.DIR_RIGHT:
            # Images are left-facing
            self.image = pygame.transform.flip(self.image, True, False)
    
    def draw(self):
        self.game.pixel_screen.blit(self.image, self.rect)
    
    def start_running(self):
        self.running = True
    def stop_running(self):
        self.running = False
    
    def jump(self):
        if not self.game.on_ground(self):
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
        self.hitbox = self.CROUCH_HITBOX
    def uncrouch(self):
        if not self.can_uncrouch():
            return
        self.crouching = False
        self.hitbox = self.HITBOX
    
    def can_uncrouch(self):
        LEFT_TILE = (self.rect.x + self.hitbox.left) // self.game.TILE_SIZE
        RIGHT_TILE = (self.rect.x + self.hitbox.right - 1) // self.game.TILE_SIZE
        ABOVE_TILE = (self.rect.y + self.hitbox.top - 4) // self.game.TILE_SIZE
        # Blocks above the player are not solid
        return (not self.game.map.is_solid_tile(LEFT_TILE, ABOVE_TILE)
                and not self.game.map.is_solid_tile(RIGHT_TILE, ABOVE_TILE))
    
    def die(self):
        self.lives -= 1
        if self.lives < 1:
            self.game.game_over()
        else:
            self.game.map.reset()
    
    def reset(self):
        self.pos.update(0, 0)
        self.vel.update(0, 0)
