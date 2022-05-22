import json
from math import floor

from boundary import Boundary
from settings import TILESIZE
from Obstacle import Obstacle
from assets import Assets
import pygame

class Map:
	def __init__(self, map_name):
		'''
		contains map information parsed from tmx file
		param map_name: name of map to parse information
		'''
		self.path = f'map/{map_name}.json'

		with open(self.path) as f:
			map_json = json.load(f)
			self._tileset_firstgids = [ts["firstgid"] for ts in map_json["tilesets"]]
			self._map_layers = map_json["layers"] 
			self._width = map_json["width"] * TILESIZE
			self._height = map_json["height"] * TILESIZE

		self._tilesets = (Assets.grass_tileset, Assets.chip_tileset, Assets.water_tileset)
		self._ground_layer = self._create_layer('ground')
		self._obstacle_layer = self._create_layer('obstacle_sprite')
		self._spawn_points = self._create_spawn_points()

	@property
	def width(self):
		return self._width

	@property
	def height(self):
		return self._height

	@property
	def size(self):
		'''return map size in (width, height)'''
		return (self._width,self._height)

	@property
	def ground_layer(self):
		'''return image of ground layers'''
		return self._ground_layer
	
	property
	def obstacle_layer(self):
		'''return image obstacle_sprite layers'''
		return self._obstacle_layer

	@property
	def spawn_points(self):
		'''return spawn points'''
		return self._spawn_points

	def _get_tile(self, tile_gid):
		'''
		returns tile information from tile_gid (tileset, area of the tile in the tileset)
		'''
		tileset = self._tilesets[-1]
		id_offset = self._tileset_firstgids[-1]

		for index, firstgid in enumerate(self._tileset_firstgids[1:], 1):
			if tile_gid < firstgid:
				tileset = self._tilesets[index - 1]
				id_offset = self._tileset_firstgids[index - 1]
				break

		tileset_cols = floor(tileset.get_width() / TILESIZE)
		tile_id = tile_gid - id_offset
		x,y = tile_id % tileset_cols, floor(tile_id / tileset_cols)
		return tileset, (x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)

	def _create_layer(self,layer_name):
		'''
		create an image from a given layer name
		parameter layer_name: layer contains this name will be render to the image
		return surface
		'''
		image = pygame.Surface((self._width, self._height), pygame.SRCALPHA)
		for layer in filter(lambda layer: layer_name in layer["name"], self._map_layers):
			for chunk in layer['chunks']:
				tile_ids, _, w, _, _ = chunk.values()
				for index, tile_gid in enumerate(tile_ids):
					if tile_gid:
						x = (index % w) 
						y = floor(index/w)
						src, area = self._get_tile(tile_gid)

						image.blit(src, (x * TILESIZE, y * TILESIZE), area)
		return image


	def init_objects(self, level):
		'''
		create game objects from object layers inside tmx file and put them into level groups
		'''
		for object_layer in filter(lambda layer: "object" in layer["name"], self._map_layers):
			layer_name = object_layer["name"]

			for chunk in object_layer["chunks"]:
				tile_ids, h, w, _, _,  = chunk.values()
				check_arr_tall = [False] * w * h
				check_arr_small = [False] * w * h
				check_arr_boundary = [False] * w * h

				for index, tile_gid in enumerate(tile_ids):
					if tile_gid:
						x = index % w
						y = floor(index / w)

						if "small" in layer_name and not check_arr_small[x + y * w]:
							self._create_obstacle_small((x, y), level, chunk, check_arr_small)
						elif "tall" in layer_name and not check_arr_tall[x + y * w]:
							self._create_obstacle_tall((x, y), level, chunk, check_arr_tall)
						elif "boundary" in layer_name and not check_arr_boundary[x + y * w]:
							self._create_boundary((x, y), level, chunk, check_arr_boundary)

	def _calculate_game_object_data(self, tile_pos, chunk, check_arr):
		'''
		calculate relavent data for game object from given chunk
		param tile_pos: tile position (in tiles)
		param chunk: tmx chunk which contains gid of tile 
		param check_arr: flag list needed for finding optimal rect area for game object
		'''
		area = self._get_area(tile_pos, chunk, check_arr)
		return (tile_pos[0] * TILESIZE, tile_pos[1] * TILESIZE), area

	def _create_obstacle_small(self, tile_pos, level, chunk, check_arr):
		'''
		create game object that are small when displayed (where it's hitbox is equal it's rect) 
		'''
		pos, area = self._calculate_game_object_data(tile_pos, chunk, check_arr)
		_, _, ow, oh = area
		
		hitbox = pygame.Rect(*pos, ow, oh)
		Obstacle(self._obstacle_layer, area, pos, hitbox, level)

	def _create_obstacle_tall(self, tile_pos, level, chunk, check_arr):
		'''
		create game object that are tall when displayed (where it's hitbox is at the bottom part of the rect) 
		'''
		pos, area = self._calculate_game_object_data(tile_pos, chunk, check_arr)
		x, y = pos
		_, _, ow, oh = area

		hitbox = pygame.Rect(x, y + oh - TILESIZE, ow, TILESIZE)
		Obstacle(self._obstacle_layer, area, pos, hitbox, level)

	def _create_boundary(self, tile_pos, level, chunk, check_arr):
		'''
		create boundary object (players can't move pass but bullets can)
		'''
		pos, area = self._calculate_game_object_data(tile_pos, chunk, check_arr)
		_, _, ow, oh = area

		hitbox = pygame.Rect(*pos, ow, oh)
		Boundary(pos, hitbox, level)

	def _get_area(self, pos, chunk, check_arr):
		'''
		get optimal area (in pixels) from given starting point
		param pos: starting position
		param chunk: tmx chunk which contains gid of tile 
		param check_arr: flag list needed for finding optimal rect area
		'''
		left, top = pos
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

	def _create_spawn_points(self):
		'''create spawn points parsed from spawn_area layer, can be used to spawn game objects such as player, enemies'''
		spawn_points = ()  
		for layer in filter(lambda layer: "spawn_area" in layer["name"], self._map_layers):
			for chunk in layer["chunks"]:
				tile_ids,_, w, _, _,  = chunk.values()
				for index, tile_gid in enumerate(tile_ids):
					### no tile? no maiden?
					if tile_gid == 0:
						continue

					x = index % w
					y = floor(index / w)
					spawn_points += ((x * TILESIZE, y * TILESIZE),)

		return spawn_points
	
