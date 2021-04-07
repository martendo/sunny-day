import pygame
from time import time
from game.actor import Actor
from game.animation import Animation

class Player(Actor):
    ACCEL = 0.5
    IN_AIR_ACCEL = 0.25
    FRICTION = 1/3
    IN_AIR_FRICTION = 0.1
    
    MAX_WALK_VELX = 1.25
    MAX_RUN_VELX = 2.5
    CROUCH_SPEED = 0.75
    MAX_VELY = 8
    
    # Small jump: 2 blocks high
    JUMP_VEL = 4
    # High jump: 3 blocks high
    HIGH_JUMP = 0.215
    # Crouch-jump: 1 block high
    CROUCH_JUMP_VEL = 3.25
    
    # Bounce after jumping on an enemy
    BOUNCE_VEL = 3
    
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
    
    START_HEALTH = 3
    START_LIVES = 5
    # Seconds of invincibility after getting hurt
    HURT_INV_LENGTH = 3
    # Length of invincibility flash in seconds
    HURT_INV_FLASH_TIME = 1/8
    HURT_INV_FLASH_ON_TIME = HURT_INV_FLASH_TIME * 2/3
    
    IMG_WIDTH = 16
    IMG_HEIGHT = 16
    SPRITESHEET = "player"
    
    IDLE_ANIMATION_SETTINGS = {
        "img": (
            0,
            1,
            2,
            1,
        ),
        "duration": (
            400,
            100,
            400,
            100,
        ),
    }
    
    MOVING_ANIMATION_SETTINGS = {
        "img": (
            3,
            4,
            5,
            6,
            7,
        ),
        "duration": 50,
    }
    
    CROUCH_IDLE_ANIMATION_SETTINGS = {
        "img": (
            8,
            9,
        ),
        "duration": 500,
    }
    
    CROUCH_MOVING_ANIMATION_SETTINGS = {
        "img": (
            10,
            8,
            11,
            9,
        ),
        "duration": (
            200,
            100,
            200,
            100,
        ),
    }
    
    MOVING_ANIM_DURATION_RANGE = 75
    BASE_MOVING_ANIM_DURATION = 25
    
    layer = 1
    
    def __init__(self, game):
        super().__init__(game, self.HITBOX)
        
        self.IDLE_ANIMATION = Animation(self, self.game, self.IDLE_ANIMATION_SETTINGS)
        self.MOVING_ANIMATION = Animation(self, self.game, self.MOVING_ANIMATION_SETTINGS)
        self.CROUCH_IDLE_ANIMATION = Animation(self, self.game, self.CROUCH_IDLE_ANIMATION_SETTINGS)
        self.CROUCH_MOVING_ANIMATION = Animation(self, self.game, self.CROUCH_MOVING_ANIMATION_SETTINGS)
        
        self.animation = self.IDLE_ANIMATION
        self.image = self.animation.get_image()
        self.set_rect(self.image.get_rect())
        
        self.lives = self.START_LIVES
        self.coins = 0
        self.reset()
    
    def update(self):
        if not self.enabled:
            return
        
        on_ground = self.game.on_ground(self)
        
        pressed = pygame.key.get_pressed()
        
        moving = False
        # Horizontal acceleration
        if pressed[self.game.MOVE_RIGHT_KEY]:
            if not self.crouching:
                if on_ground:
                    self.vel.x += self.ACCEL
                else:
                    self.vel.x += self.IN_AIR_ACCEL
            elif self.vel.x < self.CROUCH_SPEED:
                self.vel.x = self.CROUCH_SPEED
            moving = True
        if pressed[self.game.MOVE_LEFT_KEY]:
            if not self.crouching:
                if on_ground:
                    self.vel.x -= self.ACCEL
                else:
                    self.vel.x -= self.IN_AIR_ACCEL
            elif self.vel.x > -self.CROUCH_SPEED:
                if self.vel.x == self.CROUCH_SPEED:
                    self.vel.x = 0
                else:
                    self.vel.x = -self.CROUCH_SPEED
            moving = True
        
        if pressed[self.game.CROUCH_KEY] and not self.crouching:
            self.crouch()
        elif self.crouching and not pressed[self.game.CROUCH_KEY]:
            self.uncrouch()
        
        # TODO: Player's vel.x is nonzero when moving to the right into
        # a block, causing it to show the moving animation
        
        if (not self.crouching
                or (self.crouching and moving and abs(self.vel.x) > self.CROUCH_SPEED)
                or (self.crouching and not moving)):
            # Friction
            if self.vel.x > 0:
                if on_ground:
                    self.vel.x -= self.FRICTION
                else:
                    self.vel.x -= self.IN_AIR_FRICTION
                
                # Friction should not make you start moving the other way
                if self.vel.x < 0:
                    self.vel.x = 0
            elif self.vel.x < 0:
                if on_ground:
                    self.vel.x += self.FRICTION
                else:
                    self.vel.x += self.IN_AIR_FRICTION
                
                if self.vel.x > 0:
                    self.vel.x = 0
        
        # Holding down the jump key, jump for longer
        if pressed[self.game.JUMP_KEY] and not self.crouching:
            self.vel.y -= self.HIGH_JUMP
        
        # Cap velocity
        MAX_VELX = (self.MAX_RUN_VELX if pressed[self.game.RUN_KEY]
            else self.MAX_WALK_VELX)
        
        if self.vel.x > MAX_VELX:
            self.vel.x = MAX_VELX
        elif self.vel.x < -MAX_VELX:
            self.vel.x = -MAX_VELX
        
        if self.vel.y > self.MAX_VELY:
            self.vel.y = self.MAX_VELY
        
        super().update()
        
        # Collect coins
        self.block_colliding(None, self.collect_coin)
        if self.get_positioned_hitbox(self).colliderect(self.game.map.endpoint.hitbox):
            self.enabled = False
            self.game.map.finish()
        
        if self.invincible and time() >= self.invincible_end:
            self.invincible = False
        
        # Direction does not change if vel.x == 0
        if self.vel.x > 0:
            self.direction = self.game.DIR_RIGHT
        elif self.vel.x < 0:
            self.direction = self.game.DIR_LEFT
        
        # Animate!
        if not self.crouching:
            if self.vel.x != 0:
                # Set animation frame duration based on velocity
                duration = int(
                    (self.MAX_RUN_VELX - abs(self.vel.x)) / (self.MAX_RUN_VELX / self.MOVING_ANIM_DURATION_RANGE)
                    + self.BASE_MOVING_ANIM_DURATION
                )
                self.MOVING_ANIMATION.duration = duration
                self.animation = self.MOVING_ANIMATION
            else:
                self.animation = self.IDLE_ANIMATION
        else:
            # Don't show crouch-moving animation if not trying to move - crouch-slide to a stop
            if moving and self.vel.x != 0:
                self.animation = self.CROUCH_MOVING_ANIMATION
            else:
                self.animation = self.CROUCH_IDLE_ANIMATION
        # TODO: Make jump image/animation
        
        # Always set the player image because the animation may change at any time
        self.animation.update(always_set=True)
        
        # Flash when invincible (hide image)
        if (self.invincible and time() % self.HURT_INV_FLASH_TIME
                >= self.HURT_INV_FLASH_ON_TIME):
            self.image.set_alpha(0)
        else:
            self.image.set_alpha(255)
    
    def jump(self):
        if not self.game.on_ground(self):
            return
        if not self.crouching:
            self.vel.y = -self.JUMP_VEL
        else:
            self.vel.y = -self.CROUCH_JUMP_VEL
    
    # Bounce after jumping on an enemy
    def bounce(self):
        self.vel.y = -self.BOUNCE_VEL
    
    def is_stomping(self, actor):
        return (self.vel.y > 0
            and int(self.pos.y - self.vel.y) + (self.rect.height - self.hitbox.bottom)
                < (actor.rect.y + actor.hitbox.bottom) - self.game.COLLISION_OFFSET)
    
    def crouch(self):
        self.crouching = True
        self.hitbox = self.CROUCH_HITBOX
    def uncrouch(self):
        if not self.can_uncrouch():
            return
        self.crouching = False
        self.hitbox = self.HITBOX
    
    def can_uncrouch(self):
        left_pos = (self.rect.x + self.hitbox.left) // self.game.TILE_SIZE
        right_pos = (self.rect.x + self.hitbox.right - 1) // self.game.TILE_SIZE
        above_pos = (self.rect.y + self.hitbox.top - self.game.COLLISION_OFFSET) // self.game.TILE_SIZE
        # Blocks above the player are not solid
        return (not self.game.map.get_block(left_pos, above_pos).is_solid
                and not self.game.map.get_block(right_pos, above_pos).is_solid)
    
    def hurt(self, damage=1):
        if self.invincible:
            return
        
        self.health -= damage
        if self.health < 1:
            self.die()
        else:
            # Brief invincibility
            self.invincible = True
            self.invincible_end = time() + self.HURT_INV_LENGTH
    
    def die(self):
        if not self.enabled:
            return
        
        self.lives -= 1
        if self.lives < 1:
            func = self.game.game_over
        else:
            func = self.game.map.reset
        
        self.game.screen_fader.start(mid_func=func)
        self.enabled = False
    
    def collect_coin(self, block, axis):
        if block.is_coin:
            # Remove coin
            block.kill()
            del self.game.map.block_map[block.y * self.game.map.width + block.x]
            
            self.coins += 1
            
            # Got 100 coins, get an extra life
            if self.coins >= 100:
                self.lives += 1
            self.coins %= 100
        return False
    
    def reset(self, pos=(0, 0)):
        self.enabled = True
        
        self.pos.update(pos)
        self.update_rect()
        self.vel.update(0, 0)
        if self.game.map.current is not None:
            self.game.map.camera.update(self.rect)
        
        self.crouching = False
        self.direction = self.game.DIR_RIGHT
        
        self.health = self.START_HEALTH
        self.invincible = False
        
        self.animation.update()
    
    def save_state(self):
        self._saved_lives = self.lives
        self._saved_coins = self.coins
    def restore_state(self):
        if self._saved_lives < self.lives:
            self.lives = self._saved_lives
        self.coins = self._saved_coins
