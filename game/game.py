import pygame
from game.game_state import GameState
from game.map import Map
from game import block
from game.player import Player
from game import enemy
from game.camera import CameraAwareLayeredGroup
from game.status_bar import StatusBar
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
    # Height updated in __init__() for status bar
    HEIGHT = HEIGHT_PX * PX_SIZE
    GAME_WINDOW_RECT = pygame.Rect(0, 0, WIDTH, HEIGHT)
    
    COLLISION_OFFSET = 4
    
    TILESET_FILE = "tiles"
    
    IMAGE_FILES = {
        "title/": (
            "title",
            "title-sun",
        ),
    }
    
    FONT_FILE = "IBM_VGA_8x16"
    FONT_SIZE = 75
    MENU_FONT_FILE = "IBM_CGA"
    MENU_FONT_SIZE = (8 * PX_SIZE) // 2
    
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
        self.IMAGES = {}
        for directory, images in self.IMAGE_FILES.items():
            for name in images:
                self.IMAGES[name] = pygame.image.load(f"img/{directory}{name}.png")
        self.load_tileset(self.TILESET_FILE)
        self.load_spritesheets()
        
        self.FONT = pygame.font.Font(f"fonts/{self.FONT_FILE}.ttf", self.FONT_SIZE)
        self.MENU_FONT = pygame.font.Font(f"fonts/{self.MENU_FONT_FILE}.ttf", self.MENU_FONT_SIZE)
        
        self.status_bar = StatusBar(self)
        self.HEIGHT += self.status_bar.rect.height
        self.GAME_WINDOW_RECT.top += self.status_bar.rect.height
        
        pygame.display.set_icon(pygame.image.load(self.ICON))
        pygame.display.set_caption(self.NAME)
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.pixel_screen = pygame.Surface((self.WIDTH_PX, self.HEIGHT_PX))
        self.clock = pygame.time.Clock()
        self.frame = 0
        
        self.buttons = set()
        
        self.TITLE_SCREEN = TitleScreen(self)
        
        self.map = Map(self)
        self.actors = CameraAwareLayeredGroup(self.map)
        self.player = Player(self)
        # TODO: Make level selectable (level select screen)
        self.map.load(0)
    
    def load_tileset(self, file):
        self.TILESET = []
        image = pygame.image.load(f"img/{file}.png")
        width, height = image.get_size()
        tile_width = width // self.TILE_SIZE
        tile_height = height // self.TILE_SIZE
        
        for y in range(tile_height):
            for x in range(tile_width):
                rect = (x * self.TILE_SIZE, y * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
                self.TILESET.append(image.subsurface(rect))
    
    def load_spritesheets(self):
        self.SPRITESHEETS = {}
        
        self.load_spritesheet("player", Player.IMG_WIDTH, Player.IMG_HEIGHT)
        self.load_spritesheet("enemies/renky", enemy.Renky.IMG_WIDTH, enemy.Renky.IMG_HEIGHT)
    
    def load_spritesheet(self, file, spr_width, spr_height, none_colour=None):
        if none_colour is None:
            none_colour = colour.PLACEHOLDER
        
        sheet = pygame.image.load(f"img/{file}.png")
        
        frames = []
        for y in range(sheet.get_height() // spr_height):
            for x in range(sheet.get_width() // spr_width):
                rect = (x * spr_width, y * spr_height, spr_width, spr_height)
                frame = sheet.subsurface(rect)
                if frame.get_at((0, 0)) == none_colour:
                    continue
                frames.append(frame)
        self.SPRITESHEETS[file] = frames
    
    def run(self):
        self.running = True
        self.TITLE_SCREEN.init()
        
        self.coins = 0
        
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
                    
                    elif event.key == self.JUMP_KEY:
                        self.player.jump()
                    
                    elif event.key == self.CROUCH_KEY:
                        self.player.crouch()
                
                elif event.type == pygame.KEYUP:
                    if event.key == self.CROUCH_KEY:
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
            self.map.draw(self.pixel_screen)
            self.actors.draw(self.pixel_screen)
            scaled_screen = pygame.transform.scale(self.pixel_screen, self.GAME_WINDOW_RECT.size)
            self.screen.blit(scaled_screen, self.GAME_WINDOW_RECT)
            
            self.status_bar.draw(self.screen)
        
        elif self.state is GameState.GAME_OVER:
            self.screen.fill(colour.BLACK)
            text, rect = self.render_text("GAME OVER!", self.FONT, colour.WHITE, colour.BLACK)
            rect.center = (self.WIDTH / 2, self.HEIGHT / 2)
            self.screen.blit(text, rect)
            # TODO: Do something here
        
        pygame.display.update()
    
    def game_over(self):
        self.state = GameState.GAME_OVER
    
    def render_text(self, text, font, color, background=None):
        surface = font.render(text, False, color, background)
        return surface, surface.get_rect()
    
    # Determine if an actor is standing on solid ground
    def on_ground(self, actor):
        left_pos = (actor.rect.x + actor.hitbox.left) // self.TILE_SIZE
        right_pos = (actor.rect.x + actor.hitbox.right - 1) // self.TILE_SIZE
        under_pos = (actor.rect.y + actor.hitbox.bottom + self.COLLISION_OFFSET) // self.TILE_SIZE
        
        # Check every block underneath the actor, from its left to right sides
        for x in range(left_pos, right_pos + 1):
            block = self.map.get_block(x, under_pos)
            # If any block is solid, the actor is on ground
            if block.is_solid or block.is_one_way:
                return True
        # No solid block under the actor
        return False
