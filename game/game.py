import pygame
from game.game_state import GameState
from game.map import Map
from game import block
from game.player import Player
from game.camera import CameraAwareLayeredGroup
from game.title_screen import TitleScreen
from game import colour

class Game:
    NAME = "Sunny Day!"
    ICON = "img/icon.png"
    
    FPS = 30
    
    PX_SIZE = 5
    TILE_SIZE = 8
    
    WIDTH_PX = 32 * TILE_SIZE
    HEIGHT_PX = 20 * TILE_SIZE
    WIDTH = WIDTH_PX * PX_SIZE
    HEIGHT = HEIGHT_PX * PX_SIZE
    
    SPRITE_IMAGE_FILES = {
        "blocks/": (
            "sky",
            "flower-1",
            "flower-2",
            "flower-3",
            "grass",
            "brick",
        ),
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
            "player-c-m-1",
            "player-c-m-2",
        ),
        "enemies/": (
            "renky-m-1",
            "renky-m-2",
            "renky-m-3",
        ),
    }
    IMAGE_FILES = {
        "title/": (
            "title",
            "title-sun",
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
        self.state = GameState.NOT_RUNNING
        
        # Load images
        self.SPRITE_IMAGES = {}
        for directory, images in self.SPRITE_IMAGE_FILES.items():
            for name in images:
                self.SPRITE_IMAGES[name] = pygame.image.load(f"img/{directory}{name}.png")
        self.IMAGES = {}
        for directory, images in self.IMAGE_FILES.items():
            for name in images:
                self.IMAGES[name] = pygame.image.load(f"img/{directory}{name}.png")
        
        pygame.display.set_icon(pygame.image.load(self.ICON))
        pygame.display.set_caption(self.NAME)
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.pixel_screen = pygame.Surface((self.WIDTH_PX, self.HEIGHT_PX))
        self.clock = pygame.time.Clock()
        self.frame = 0
        
        # TODO: Choose/Make a more fitting font
        self.FONT = pygame.font.Font(None, 100)
        
        self.buttons = set()
        
        self.TITLE_SCREEN = TitleScreen(self)
        
        self.map = Map(self)
        self.actors = CameraAwareLayeredGroup(self.map)
        self.player = Player(self, (7 * self.TILE_SIZE, 5 * self.TILE_SIZE))
        # TODO: Make level selectable (level select screen)
        self.map.load(0)
    
    def run(self):
        self.running = True
        self.TITLE_SCREEN.init()
        
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
                self.state = GameState.NOT_RUNNING
                return
            
            if self.state is not GameState.IN_LEVEL:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.is_hovered(event.pos):
                            button.click()
            
            else:
                if event.type == pygame.KEYDOWN:
                    # Move a pixel right away if stopped so a quick press will nudge the player
                    if event.key == self.MOVE_RIGHT_KEY and self.player.vel.x == 0:
                        self.player.pos.x += 1
                        self.player.direction = self.DIR_RIGHT
                    elif event.key == self.MOVE_LEFT_KEY and self.player.vel.x == 0:
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
        if self.state is GameState.TITLE_SCREEN:
            self.TITLE_SCREEN.update()
        
        elif self.state is GameState.IN_LEVEL:
            # Apply gravity to all actors
            for actor in self.actors:
                actor.vel.y += self.GRAVITY
            
            self.map.update()
            self.player.update()
    
    def draw(self):
        if self.state is GameState.TITLE_SCREEN:
            self.TITLE_SCREEN.draw()
        
        elif self.state is GameState.IN_LEVEL:
            self.screen.fill(colour.PLACEHOLDER)
            self.map.blocks.draw(self.pixel_screen)
            self.actors.draw(self.pixel_screen)
            scaled_screen = pygame.transform.scale(self.pixel_screen, (self.screen.get_size()))
            self.screen.blit(scaled_screen, self.screen.get_rect())
        
        elif self.state is GameState.GAME_OVER:
            self.screen.fill(colour.BLACK)
            text, rect = self.render_text("GAME OVER!", colour.WHITE, colour.BLACK)
            rect.center = (self.WIDTH / 2, self.HEIGHT / 2)
            self.screen.blit(text, rect)
            # TODO: Do something here
        
        pygame.display.update()
    
    def game_over(self):
        self.state = GameState.GAME_OVER
    
    def render_text(self, text, color, background=None):
        surface = self.FONT.render(text, False, color, background)
        return surface, surface.get_rect()
    
    # Determine if an actor is standing on solid ground
    def on_ground(self, actor):
        LEFT_TILE = (actor.rect.x + actor.hitbox.left) // self.TILE_SIZE
        RIGHT_TILE = (actor.rect.x + actor.hitbox.right - 1) // self.TILE_SIZE
        UNDER_TILE = (actor.rect.y + actor.hitbox.bottom + 4) // self.TILE_SIZE
        # No solid tile under the actor
        return (self.map.is_solid_tile(LEFT_TILE, UNDER_TILE)
                or self.map.is_solid_tile(RIGHT_TILE, UNDER_TILE))
