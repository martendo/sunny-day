import pygame
from game.map import Map
from game import block
from game.player import Player

class Game:
    NAME = "Sunny Day!"
    ICON = "img/icon.png"
    
    FPS = 30
    
    PX_SIZE = 5
    TILE_PX = 8
    TILE_SIZE = TILE_PX * PX_SIZE
    
    WIDTH = 32 * TILE_SIZE
    HEIGHT = 20 * TILE_SIZE
    
    # This colour should not be seen
    PLACEHOLDER_COLOUR = (255, 0, 255)
    
    IMAGE_FILES = {
        "player/": (
            "player-1",
            "player-2",
            "player-3",
            "player-m-1",
            "player-m-2",
            "player-m-3",
            "player-m-4",
            "player-m-5",
            "player-c-1",
            "player-c-2",
        ),
        "blocks/": (
            "sky",
            "flower-1",
            "flower-2",
            "flower-3",
            "grass",
            "brick",
        ),
    }
    
    GRAVITY = 0.5
    
    DIR_LEFT = -1
    DIR_RIGHT = +1
    
    MOVE_LEFT_KEY = pygame.K_a
    CROUCH_KEY = pygame.K_s
    MOVE_RIGHT_KEY = pygame.K_d
    RUN_KEY = pygame.K_LSHIFT
    JUMP_KEY = pygame.K_SPACE
    
    def __init__(self):
        pygame.init()
        
        self.running = False
        self.playing = False
        
        # Load and scale images
        self.IMAGES = {}
        for directory, images in self.IMAGE_FILES.items():
            for name in images:
                image = pygame.image.load(f"img/{directory}{name}.png")
                self.IMAGES[name] = pygame.transform.scale(image, (image.get_width() * self.PX_SIZE, image.get_height() * self.PX_SIZE))
        
        pygame.display.set_icon(pygame.image.load(self.ICON))
        pygame.display.set_caption(self.NAME)
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.frame = 0
        
        self.actors = pygame.sprite.Group()
        
        self.player = Player(self, (7 * self.TILE_PX, 5 * self.TILE_PX))
        
        # TODO: Make level selectable (level select screen)
        self.map = Map(0, self)
        # TODO: Make maps scrollable
        self.scroll = pygame.Vector2(0, 0)
    
    def run(self):
        self.running = True
        self.playing = True
        
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.FPS)
            self.frame += 1
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            
            if self.playing:
                if event.type == pygame.KEYDOWN:
                    # Move a pixel right away so a quick press will nudge the player
                    if event.key == self.MOVE_RIGHT_KEY:
                        self.player.pos.x += 1
                        self.player.direction = self.DIR_RIGHT
                    elif event.key == self.MOVE_LEFT_KEY:
                        self.player.pos.x -= 1
                        self.player.direction = self.DIR_LEFT
                    
                    elif event.key == self.RUN_KEY:
                        self.player.start_running()
                    
                    elif event.key == self.JUMP_KEY:
                        self.player.jump()
                    
                    elif event.key == self.CROUCH_KEY:
                        self.player.crouch()
                
                elif event.type == pygame.KEYUP:
                    if event.key == self.RUN_KEY:
                        self.player.stop_running()
                    
                    elif event.key == self.JUMP_KEY:
                        self.player.release_jump()
                    
                    elif event.key == self.CROUCH_KEY:
                        self.player.uncrouch()
    
    def update(self):
        if self.playing:
            # Apply gravity to all actors
            for actor in self.actors:
                actor.vel.y += self.GRAVITY
            
            self.map.update()
            self.player.update()
    
    def draw(self):
        if self.playing:
            self.screen.fill(self.PLACEHOLDER_COLOUR)
            self.map.draw()
            self.player.draw()
        
        pygame.display.update()
    
    def game_over(self):
        self.playing = False
        # TODO: Do something here
        self.screen.fill((255, 100, 100))
    
    # Determine if an actor can jump (is standing on solid ground)
    def can_jump(self, actor):
        LEFT_TILE = (actor.rect.x + actor.hitbox.left) // self.TILE_SIZE
        RIGHT_TILE = (actor.rect.x + actor.hitbox.right - 1) // self.TILE_SIZE
        UNDER_TILE = (actor.rect.y + actor.hitbox.bottom + self.PX_SIZE * 4) // self.TILE_SIZE
        # No solid tile under the actor, don't allow jump
        return (self.map.is_solid_tile(LEFT_TILE, UNDER_TILE)
                or self.map.is_solid_tile(RIGHT_TILE, UNDER_TILE))
