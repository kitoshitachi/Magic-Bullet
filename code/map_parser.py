from collections import namedtuple
import json
from math import floor
from settings import TILESIZE
from Obstacle import Obstacle
from tilesets import Tilesets
from tile import Tile
from wall import Wall
import pygame

TileInfo = namedtuple("TileInfo", ["tile_set", "tile_id", "x", "y"])

class MapParser():
  def __init__(self, map_name):
    self.path = f'map/{map_name}.json'

    self.tilesets = [Tilesets.grass_tileset, Tilesets.chip_tileset, Tilesets.water_tileset]

    with open(self.path) as f:
      self.map_json = json.load(f)
      self.obstacle_image = self._create_obstacle_image()

  def create_map_ground_image(self):
    tile_w = self.map_json["tilewidth"]
    tile_h = self.map_json["tileheight"]

    map_image = pygame.Surface((
        self.map_json["width"] * tile_w, self.map_json["height"] * tile_h))

    for layer in self.map_json['layers']:
      if "ground" not in layer["name"]:
        continue

      for chunk in layer["chunks"]:
          w = chunk["width"]
          offset_x = chunk["x"]
          offset_y = chunk["y"]
          for index, tile_gid in enumerate(chunk["data"]):
              ### no tile? no maiden?
              if tile_gid == 0:
                continue

              x = index % w
              y = floor(index / w)

              tile_info = self.get_tile_info_from_id(tile_gid, tile_w)

              map_image.blit(tile_info.tile_set, ((x + offset_x) * tile_w, (y + offset_y) * tile_h),
                             (tile_info.x * tile_w, tile_info.y * tile_h, tile_w, tile_h))
    return map_image


  def _create_obstacle_image(self):
      tile_w = self.map_json["tilewidth"]
      tile_h = self.map_json["tileheight"]

      image = pygame.Surface((
          self.map_json["width"] * tile_w, self.map_json["height"] * tile_h), pygame.SRCALPHA)

      for layer in self.map_json['layers']:
        if "obstacle_sprite" not in layer["name"]:
          continue

        for chunk in layer["chunks"]:
            w = chunk["width"]
            offset_x = chunk["x"]
            offset_y = chunk["y"]
            for index, tile_gid in enumerate(chunk["data"]):
                ### no tile? no maiden?
                if tile_gid == 0:
                  continue

                x = index % w
                y = floor(index / w)

                tile_info = self.get_tile_info_from_id(tile_gid, tile_w)

                image.blit(tile_info.tile_set, ((x + offset_x) * tile_w, (y + offset_y) * tile_h),
                              (tile_info.x * tile_w, tile_info.y * tile_h, tile_w, tile_h))
      return image

  def get_tile_info_from_id(self, tile_gid, tile_width) -> TileInfo:
    tilesets_info = self.map_json["tilesets"]
    tileset = self.tilesets[-1]
    id_offset = tilesets_info[-1]["firstgid"]

    for index, tileset_info in enumerate(tilesets_info[1:], 1):
      if tile_gid < tileset_info["firstgid"]:
        tileset = self.tilesets[index - 1]
        id_offset = tilesets_info[index - 1]["firstgid"]
        break

    tileset_cols = floor(tileset.get_width() / tile_width)
    tile_id = tile_gid - id_offset
    return TileInfo(tileset, tile_id, tile_id % tileset_cols, floor(tile_id / tileset_cols))

  def init_objects(self, level):
    for layer in self.map_json['layers']:
      layer_name = layer["name"]

      if "object" not in layer_name:
        continue
      
      for chunk in layer["chunks"]:
          w = chunk["width"]
          h = chunk["width"]
          check_arr = [False] * w * h 
          offset_x = chunk["x"]
          offset_y = chunk["y"]

          for index, tile_gid in enumerate(chunk["data"]):
            ### no tile? no maiden?
            if tile_gid == 0:
              continue

            x = index % w
            y = floor(index / w)

            if "small" in layer_name:
              self._create_obstacle_small((x, y), (offset_x, offset_y), level)
            if "tall" in layer_name and not check_arr[x + y * w]:
              self._create_obstacle_tall((x, y), (offset_x, offset_y), level, chunk, check_arr, tile_gid)

      
            # tile_info = self.get_tile_info_from_id(tile_gid, TILESIZE)
    
            # if "object" in layer_name:
            #   Wall(((x + offset_x) * TILESIZE, (y + offset_y) * TILESIZE), level),
            # elif "obstacle" in layer_name:
            #   Tile(tile_info.tile_set, tile_info.tile_id, ((x + offset_x) * TILESIZE, (y + offset_y) * TILESIZE), level)

  def _create_obstacle_small(self, tile_pos, tile_offset_pos, level):
    x, y = tile_pos
    offset_x, offset_y = tile_offset_pos
    position = ((x + offset_x) * TILESIZE, (y + offset_y) * TILESIZE)
    hitbox = pygame.Rect(position[0], position[1], TILESIZE, TILESIZE)
    area = (position[0], position[1], TILESIZE, TILESIZE)
    Obstacle(self.obstacle_image, area, position, hitbox, level)

  def _create_obstacle_tall(self, tile_pos, tile_offset_pos, level, chunk, check_arr, tile_gid):
    x, y = tile_pos
    offset_x, offset_y = tile_offset_pos
    px, py = ((x + offset_x) * TILESIZE, (y + offset_y) * TILESIZE)

    area = self._get_area(x, y, chunk, check_arr)
    _, _, ow, oh = area

    hitbox = pygame.Rect(px, py + oh - TILESIZE, ow, TILESIZE)
    Obstacle(self.obstacle_image, area, (px, py), hitbox, level)

  def _get_area(self, left, top, chunk, check_arr):
    chunk_arr = chunk["data"]
    w = chunk["width"]
    h = chunk["width"]

    current_gid = chunk_arr[left + top * w]
    right = left
    bottom = top

    found_right = False
    found_bottom = False

    while not found_right or not found_bottom:
      if right == w:
        right -= 1
        found_right = True

      if bottom == h:
        bottom -= 1
        found_bottom = True

      if not found_right:
        for gid in chunk_arr[right + top * w : right + bottom * w + 1 : w]:
          if gid != current_gid:
            right -= 1
            found_right = True
            break

      if not found_bottom:
        for gid in chunk_arr[left + bottom * w : right + bottom * w + 1]:
          if gid != current_gid:
            bottom -= 1
            found_bottom = True
            break

      if not found_right:
         for index in range(right + top * w, right + bottom * w + 1, w):
           check_arr[index] = True
      
      if not found_bottom:
         for index in range(left + bottom * w, right + bottom * w + 1):
           check_arr[index] = True

      if not found_right: 
        right += 1

      if not found_bottom:
        bottom += 1

    return (left * TILESIZE, top * TILESIZE, (right - left + 1) * TILESIZE, (bottom - top + 1) * TILESIZE)
