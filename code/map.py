import json
from math import floor

from boundary import Boundary
from settings import TILESIZE
from Obstacle import Obstacle
from assets import Assets
import pygame

class Map():
	def __init__(self, map_name):
		self.path = f'map/{map_name}.json'

		with open(self.path) as f:
			map_json = json.load(f)
			self.tileset_firstgids = [ts["firstgid"] for ts in map_json["tilesets"]]
			self.map_layers = map_json["layers"] 
			self.width = map_json["width"] * TILESIZE
			self.height = map_json["height"] * TILESIZE

		self.tilesets = [Assets.grass_tileset, Assets.chip_tileset, Assets.water_tileset]
		self.ground = self.create_layer('ground')
		self.obstacle = self.create_layer('obstacle_sprite')
		self.spawn_points = self.create_spawn_points()

	@property
	def size(self):
		'''return (width, height)'''
		return (self.width,self.height)

	def create_layer(self,layer_name):
		'''
		parameter layer_name: the name of layer
		return surface
		'''
		image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
		layers = filter(lambda layer: layer_name in layer["name"], self.map_layers)
		for layer in layers:
			for chunk in layer['chunks']:
				tile_ids, _, w, _, _ = chunk.values()
				for index, tile_gid in enumerate(tile_ids):
					if tile_gid:
						x = (index % w) 
						y = floor(index/w)
						src, area = self.get_tile(tile_gid)

						image.blit(src, (x * TILESIZE, y * TILESIZE), area)
		return image

	def get_tile(self, tile_gid):
		'''return tileset, area'''
		tileset = self.tilesets[-1]
		id_offset = self.tileset_firstgids[-1]

		for index, firstgid in enumerate(self.tileset_firstgids[1:], 1):
			if tile_gid < firstgid:
				tileset = self.tilesets[index - 1]
				id_offset = self.tileset_firstgids[index - 1]
				break

		tileset_cols = floor(tileset.get_width() / TILESIZE)
		tile_id = tile_gid - id_offset
		x,y = tile_id % tileset_cols, floor(tile_id / tileset_cols)
		return tileset, (x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)

	def init_objects(self, level):
		for object_layer in filter(lambda layer: "object" in layer["name"], self.map_layers):
			layer_name = object_layer["name"]

			for chunk in object_layer["chunks"]:
				tile_ids, h, w, offset_x, offset_y,  = chunk.values()
				check_arr_tall = [False] * w * h
				check_arr_small = [False] * w * h
				check_arr_boundary = [False] * w * h

				for index, tile_gid in enumerate(tile_ids):
					### no tile? no maiden?
					if tile_gid == 0:
						continue

					x = index % w
					y = floor(index / w)

					if "small" in layer_name and not check_arr_small[x + y * w]:
						self._create_obstacle_small((x, y), (offset_x, offset_y), level, chunk, check_arr_small)
					elif "tall" in layer_name and not check_arr_tall[x + y * w]:
						self._create_obstacle_tall((x, y), (offset_x, offset_y), level, chunk, check_arr_tall)
					elif "boundary" in layer_name and not check_arr_boundary[x + y * w]:
						self._create_boundary((x, y), (offset_x, offset_y), level, chunk, check_arr_boundary)

	def _create_obstacle_small(self, tile_pos, tile_offset_pos, level, chunk, check_arr):
		x, y = tile_pos
		pos_x, pos_y = self._calculate_postion(tile_pos, tile_offset_pos)
		
		area = self._get_area(x, y, chunk, check_arr)
		_, _, ow, oh = area
		
		hitbox = pygame.Rect(pos_x, pos_y, ow, oh)
		Obstacle(self.obstacle, area, (pos_x, pos_y), hitbox, level)

	def _create_obstacle_tall(self, tile_pos, tile_offset_pos, level, chunk, check_arr):
		x, y = tile_pos
		pos_x, pos_y = self._calculate_postion(tile_pos, tile_offset_pos)

		area = self._get_area(x, y, chunk, check_arr)
		_, _, ow, oh = area

		hitbox = pygame.Rect(pos_x, pos_y + oh - TILESIZE, ow, TILESIZE)
		Obstacle(self.obstacle, area, (pos_x, pos_y), hitbox, level)

	def _create_boundary(self, tile_pos, tile_offset_pos, level, chunk, check_arr):
		x, y = tile_pos
		pos_x, pos_y = self._calculate_postion(tile_pos, tile_offset_pos)

		_, _, ow, oh = self._get_area(x, y, chunk, check_arr)

		hitbox = pygame.Rect(pos_x, pos_y, ow, oh)
		Boundary((pos_x, pos_y), hitbox, level)

	def _calculate_postion(self, tile_pos, tile_offset_pos):
		return ((tile_pos[0] + tile_offset_pos[0]) * TILESIZE, (tile_pos[1] + tile_offset_pos[1]) * TILESIZE)

	def _get_area(self, left, top, chunk, check_arr):
		tile_ids, h, w, _, _,  = chunk.values()

		current_gid = tile_ids[left + top * w]
		right = left
		bottom = top

		found_right = False
		found_bottom = False

		while not found_right or not found_bottom:
			if right == w or tile_ids[right + top * w] != current_gid:
				right -= 1
				found_right = True

			if bottom == h or tile_ids[left + bottom * w] != current_gid:
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
				tile_ids,h, w, offset_x, offset_y,  = chunk.values()
				for index, tile_gid in enumerate(tile_ids):
					### no tile? no maiden?
					if tile_gid == 0:
						continue

					x = index % w
					y = floor(index / w)
					spawn_points.append((x * TILESIZE, y * TILESIZE))

		return spawn_points