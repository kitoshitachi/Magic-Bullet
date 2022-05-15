from math import floor
import pygame
from tilesets import Tilesets
from game_object import GameObject
from settings import *

class Tile(GameObject):
  def __init__(self, tile_set, tile_id, pos, level):
    super().__init__(group=[level.group_visible])

    self.tileset = tile_set
    self.rect = pygame.Rect(pos[0], pos[1], TILESIZE, TILESIZE)
    self.hitbox = self.rect.inflate(0,0)
    
    tileset_w = self.tileset.get_width()
    tileset_cols = floor(tileset_w / TILESIZE)
    tile_x = tile_id % tileset_cols
    tile_y = floor(tile_id / tileset_cols)
    self.area = (tile_x * TILESIZE, tile_y * TILESIZE, TILESIZE, TILESIZE)

  def render(self, offset):
    self.display_surface.blit(self.tileset, self.rect.topleft - offset, self.area)
