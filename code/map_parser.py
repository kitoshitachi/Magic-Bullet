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
ChunkProps = namedtuple("ChunkProps", ["width", "height", "offset_x", "offset_y", "tile_ids"])

class MapParser():
  def __init__(self, map_name):
    self.path = f'map/{map_name}.json'

    with open(self.path) as f:
      map_json = json.load(f)
      self.tileset_firstgids = [ts["firstgid"] for ts in map_json["tilesets"]]
      self.tilesets = [Tilesets.grass_tileset, Tilesets.chip_tileset, Tilesets.water_tileset]
      self.map_layers = map_json["layers"] 
      self.map_w = map_json["width"]
      self.map_h = map_json["height"]
      self.obstacle_image = self._create_obstacle_image()

  def _get_chunk_props(self, chunk) -> ChunkProps:
    return ChunkProps(chunk["width"], chunk["height"], chunk["x"], chunk["y"], chunk["data"])

  def create_map_ground_image(self):
    image = pygame.Surface((self.map_w * TILESIZE, self.map_h * TILESIZE))

    for ground_layer in filter(lambda layer: "ground" in layer["name"], self.map_layers):
      for chunk in ground_layer["chunks"]:
          w, _, offset_x, offset_y, tile_ids = self._get_chunk_props(chunk)
          for index, tile_gid in enumerate(tile_ids):
              ### no tile? no maiden?
              if tile_gid == 0:
                continue

              x = index % w
              y = floor(index / w)

              tile_info = self.get_tile_info_from_id(tile_gid, TILESIZE)

              image.blit(tile_info.tile_set, ((x + offset_x) * TILESIZE, (y + offset_y) * TILESIZE),
                             (tile_info.x * TILESIZE, tile_info.y * TILESIZE, TILESIZE, TILESIZE))
    return image


  def _create_obstacle_image(self):
      image = pygame.Surface((self.map_w * TILESIZE, self.map_h * TILESIZE), pygame.SRCALPHA)

      for layer in filter(lambda layer: "obstacle_sprite" in layer["name"], self.map_layers):
        for chunk in layer["chunks"]:
            w, _, offset_x, offset_y, tile_ids = self._get_chunk_props(chunk)
            for index, tile_gid in enumerate(tile_ids):
                if tile_gid == 0:
                  continue

                x = index % w
                y = floor(index / w)

                tile_info = self.get_tile_info_from_id(tile_gid, TILESIZE)

                image.blit(tile_info.tile_set, ((x + offset_x) * TILESIZE, (y + offset_y) * TILESIZE),
                           (tile_info.x * TILESIZE, tile_info.y * TILESIZE, TILESIZE, TILESIZE))
      return image

  def get_tile_info_from_id(self, tile_gid, tile_width) -> TileInfo:
    tileset = self.tilesets[-1]
    id_offset = self.tileset_firstgids[-1]

    for index, firstgid in enumerate(self.tileset_firstgids[1:], 1):
      if tile_gid < firstgid:
        tileset = self.tilesets[index - 1]
        id_offset = self.tileset_firstgids[index - 1]
        break

    tileset_cols = floor(tileset.get_width() / tile_width)
    tile_id = tile_gid - id_offset
    return TileInfo(tileset, tile_id, tile_id % tileset_cols, floor(tile_id / tileset_cols))

  def init_objects(self, level):
    for object_layer in filter(lambda layer: "object" in layer["name"], self.map_layers):
      layer_name = object_layer["name"]

      for chunk in object_layer["chunks"]:
          w, h, offset_x, offset_y, tile_ids = self._get_chunk_props(chunk)
          check_arr = [False] * w * h 

          for index, tile_gid in enumerate(tile_ids):
            ### no tile? no maiden?
            if tile_gid == 0:
              continue

            x = index % w
            y = floor(index / w)

            if "small" in layer_name:
              self._create_obstacle_small((x, y), (offset_x, offset_y), level)
            if "tall" in layer_name and not check_arr[x + y * w]:
              self._create_obstacle_tall((x, y), (offset_x, offset_y), level, chunk, check_arr)

  def _create_obstacle_small(self, tile_pos, tile_offset_pos, level):
    x, y = tile_pos
    offset_x, offset_y = tile_offset_pos
    position = ((x + offset_x) * TILESIZE, (y + offset_y) * TILESIZE)
    hitbox = pygame.Rect(position[0], position[1], TILESIZE, TILESIZE)
    area = (position[0], position[1], TILESIZE, TILESIZE)
    Obstacle(self.obstacle_image, area, position, hitbox, level)

  def _create_obstacle_tall(self, tile_pos, tile_offset_pos, level, chunk, check_arr):
    x, y = tile_pos
    offset_x, offset_y = tile_offset_pos
    px, py = ((x + offset_x) * TILESIZE, (y + offset_y) * TILESIZE)

    area = self._get_area(x, y, chunk, check_arr)
    _, _, ow, oh = area

    hitbox = pygame.Rect(px, py + oh - TILESIZE, ow, TILESIZE)
    Obstacle(self.obstacle_image, area, (px, py), hitbox, level)

  def _get_area(self, left, top, chunk, check_arr):
    w, h, _, _, tile_ids = self._get_chunk_props(chunk)

    current_gid = tile_ids[left + top * w]
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
        for gid in tile_ids[right + top * w : right + bottom * w + 1 : w]:
          if gid != current_gid:
            right -= 1
            found_right = True
            break

      if not found_bottom:
        for gid in tile_ids[left + bottom * w : right + bottom * w + 1]:
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

  def create_spawn_points(self):
    spawn_points = []  
    for layer in filter(lambda layer: "spawn_area" in layer["name"], self.map_layers):
      for chunk in layer["chunks"]:
          w, _, offset_x, offset_y, tile_ids = self._get_chunk_props(chunk)
          for index, tile_gid in enumerate(tile_ids):
              ### no tile? no maiden?
              if tile_gid == 0:
                continue

              x = index % w
              y = floor(index / w)
              spawn_points.append((x * TILESIZE, y * TILESIZE))

    return spawn_points
  

