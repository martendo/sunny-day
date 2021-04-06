import pygame
import json
from game.game_state import GameState
from game.block import Block
from game.enemy import TYPES as ENEMY_TYPES
from game.camera import Camera, CameraAwareLayeredGroup
from game import colour

class MissingMapDataError(Exception):
    pass

class EndPoint(pygame.sprite.Sprite):
    def __init__(self, game, pos):
        self.game = game
        self.image = self.game.IMAGES["endpoint"]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
    
    def draw(self, surface):
        surface.blit(self.image, self.rect.move(-self.game.map.camera.pos))

class Map:
    MAIN_TILESET = "maps/tiles.json"
    
    EMPTY_TILE = 0
    
    TILE_FLIP_H = 0x80000000
    TILE_FLIP_V = 0x40000000
    TILE_FLIP_D = 0x20000000
    
    def __init__(self, game):
        self.game = game
        
        self.tilesets = {}
        
        self.EMPTY_BLOCK = Block(self.game, self, 0, 0, 0, {
            "h": False,
            "v": False,
            "d": False,
        })
        
        self.current = None
        self.backgroundColour = colour.PLACEHOLDER
        
        self.camera = Camera(self.game)
        self.blocks = CameraAwareLayeredGroup(self)
        self.enemies = CameraAwareLayeredGroup(self)
        self.block_map = {}
        self.spawn_point = (0, 0)
        self.endpoint = None
    
    def load(self, num):
        self.current = num
        
        with open(f"maps/{num}.json", "r") as file:
            self.data = json.load(file)
        
        # Background colour
        self.backgroundColour = pygame.Color(self.data["backgroundcolor"])
        
        # Tilemap
        for layer in self.data["layers"]:
            if layer["type"] == "tilelayer":
                break
        else:
            raise MissingMapDataError(f"No tile layer found in game/maps/{num}.json")
        self.tilemap = layer["data"]
        self.width = self.data["width"]
        self.height = self.data["height"]
        
        # Enemy data
        for layer in self.data["layers"]:
            if layer["type"] == "objectgroup":
                break
        else:
            raise MissingMapDataError(f"No object layer found in game/maps/{num}.json")
        self.objects = layer["objects"]
        self.enemy_data = []
        for obj in self.objects:
            if obj["type"] == "SpawnPoint":
                self.spawn_point = (obj["x"], obj["y"])
            elif obj["type"] == "EndPoint":
                self.endpoint = EndPoint(self.game, (obj["x"], obj["y"]))
            elif "gid" in obj:
                self.enemy_data.append(obj)
        
        self.reset()
    
    def create_blocks(self):
        self.blocks.empty()
        self.block_map = {}
        for y in range(self.height):
            for x in range(self.width):
                pos = y * self.width + x
                
                tile_id, tileset, flip = self._resolve_gid(self.tilemap[pos])
                if tile_id == self.EMPTY_TILE:
                    continue
                
                block = Block(self.game, self, x, y, tile_id - tileset["firstgid"], flip)
                self.blocks.add(block)
                self.block_map[pos] = block
    
    def create_enemies(self):
        self.game.actors.remove(self.enemies)
        self.enemies.empty()
        for enemy in self.enemy_data:
            tile_id, tileset, flip = self._resolve_gid(enemy["gid"])
            name = self.get_tile(
                tile_id - tileset["firstgid"],
                "maps/{}".format(tileset["source"])
            )["type"]
            self.enemies.add(ENEMY_TYPES[name](
                self.game,
                (enemy["x"], enemy["y"])
            ))
    
    def _resolve_gid(self, gid):
        flip = {
            "h": bool(gid & self.TILE_FLIP_H),
            "v": bool(gid & self.TILE_FLIP_V),
            "d": bool(gid & self.TILE_FLIP_D),
        }
        # Clear flipping flags
        gid &= ~(self.TILE_FLIP_H | self.TILE_FLIP_V | self.TILE_FLIP_D)
        
        for tileset in reversed(self.data["tilesets"]):
            if tileset["firstgid"] <= gid:
                return gid, tileset, flip
        
        return self.EMPTY_TILE, None, flip
    
    def get_tileset(self, tileset):
        try:
            return self.tilesets[tileset]
        except KeyError:
            with open(tileset, "r") as file:
                data = json.load(file)
            self.tilesets[tileset] = data
            return data
    
    def get_tile(self, tile_id, tileset=None):
        if tileset is None:
            tileset = self.MAIN_TILESET
        for tile in self.get_tileset(tileset)["tiles"]:
            if tile["id"] == tile_id:
                return tile
        return None
    
    def get_block(self, x, y):
        if x < 0 or y < 0:
            return self.EMPTY_BLOCK
        try:
            return self.block_map[y * self.width + x]
        except KeyError:
            return self.EMPTY_BLOCK
    
    def update(self):
        self.blocks.update()
        self.enemies.update()
        self.camera.update(self.game.player.rect)
    
    def draw(self, surface):
        surface.fill(self.backgroundColour)
        self.endpoint.draw(surface)
        self.blocks.draw(surface)
    
    def finish(self):
        self.game.level_completion[self.current - 1] = True
        self.game.screen_fader.start(**{
            "mid_func": self.end_level,
        })
    def end_level(self):
        self.game.state = GameState.LEVEL_SELECT
        self.game.player.reset()
        self.game.save()
    
    def reset(self):
        self.create_blocks()
        self.create_enemies()
        self.game.player.reset(self.spawn_point)
