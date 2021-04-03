import pygame
from game import block
from game import enemy
from game.camera import CameraAwareGroup

class Map:
    WIDTH_POS = 0
    WIDTH_END = WIDTH_POS + 2
    
    HEIGHT_POS = WIDTH_END
    HEIGHT_END = HEIGHT_POS + 2
    
    MAP_DATA_POS = HEIGHT_END
    
    NUM_ENEMIES_POS = 0
    NUM_ENEMIES_END = NUM_ENEMIES_POS + 2
    
    ENEMY_DATA_POS = NUM_ENEMIES_END
    
    ENEMY_ENTRY_SIZE = 1 + (2 * 2)
    
    def __init__(self, game):
        self.game = game
        
        self.current = None
        self.camera = pygame.Vector2(0, 0)
        self.blocks = CameraAwareGroup(self)
        self.enemies = CameraAwareGroup(self)
    
    def load(self, num):
        # Map data
        with open(f"maps/{num}.smd", "rb") as file:
            self.map_data = file.read()
        
        self.width = int.from_bytes(self.map_data[self.WIDTH_POS : self.WIDTH_END], byteorder="little")
        self.height = int.from_bytes(self.map_data[self.HEIGHT_POS : self.HEIGHT_END], byteorder="little")
        
        self.MAP_DATA_END = self.MAP_DATA_POS + (self.width * self.height)
        self.tilemap = self.map_data[self.MAP_DATA_POS : self.MAP_DATA_END]
        
        # Enemy data
        with open(f"maps/{num}.sed", "rb") as file:
            enemy_data = file.read()
        
        self.num_enemies = int.from_bytes(enemy_data[self.NUM_ENEMIES_POS : self.NUM_ENEMIES_END], byteorder="little")
        
        self.ENEMY_DATA_END = self.ENEMY_DATA_POS + (self.ENEMY_ENTRY_SIZE * self.num_enemies)
        self.enemy_data = enemy_data[self.ENEMY_DATA_POS : self.ENEMY_DATA_END]
        
        self.reset()
    
    def create_blocks(self):
        for y in range(self.height):
            for x in range(self.width):
                self.blocks.add(block.TYPES[self.get_tile(x, y)](self.game, x, y))
    
    def create_enemies(self):
        for i in range(self.num_enemies):
            cur_enemy = self.get_enemy(i)
            self.enemies.add(enemy.TYPES[cur_enemy["type"]](
                self.game,
                pygame.Vector2(*map(lambda x: x * self.game.TILE_SIZE, cur_enemy["pos"]))
            ))
    
    def get_tile(self, x, y):
        try:
            return self.tilemap[y * self.width + x]
        except:
            return 0
    
    def is_solid_tile(self, x, y):
        return self.get_tile(x, y) >= block.SOLIDS_START
    
    def get_enemy(self, num):
        enemy_pos = num * self.ENEMY_ENTRY_SIZE
        enemy_data = self.enemy_data[enemy_pos : enemy_pos + self.ENEMY_ENTRY_SIZE]
        return {
            "type": int(enemy_data[0]),
            "pos": pygame.Vector2( # Positions are by tile (1 tile = Game.TILE_SIZE screen pixels)
                int.from_bytes(enemy_data[1:3], byteorder="little"),
                int.from_bytes(enemy_data[3:5], byteorder="little"),
            ),
        }
    
    def update(self):
        self.blocks.update()
        self.enemies.update()
    
    def reset(self):
        self.blocks.empty()
        self.enemies.empty()
        self.create_blocks()
        self.create_enemies()
        self.game.player.reset()
