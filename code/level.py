import random
from NPC import NPC
import json
import pygame
from map_parser import MapParser
from settings import *
from minimap import Minimap 
from player import Player
from debug import debug

class Level:
	def __init__(self, map_name):
		# get the display surface 
		self.display_surface = pygame.display.get_surface()

		# sprite group setup
		map_parser = MapParser(map_name)
		self.map_ground_image = map_parser.create_map_ground_image()
		self.visible_sprites = YSortCameraGroup(self)
		self.obstacle_sprites = pygame.sprite.Group()
		self.bullet_sprites = pygame.sprite.Group()
		self.player_sprites = pygame.sprite.Group()
		self.NPC_sprites = pygame.sprite.Group()
		# sprite setup
		self.spawn_points = map_parser.create_spawn_points()
		self.create_player()
		self.create_NPC()
		# others
		self.createNPC_time = 0
<<<<<<< HEAD


		map_parser.init_objects(self)
		# others
		self.minimap = Minimap((16, 16), self.player)

	def create_map(self):
		for row_index,row in enumerate(WORLD_MAP):
			for col_index, col in enumerate(row):
				x = col_index * TILESIZE
				y = row_index * TILESIZE
				if col == ' ':
					self.No_sprites.append((x,y))
=======
		map_parser.init_objects(self)
		# others
		self.minimap = Minimap((16, 16), self.player, map_parser.create_minimap_image())
>>>>>>> 03df69a03265a2e25cdfdb1e5a8f867c9fae577d

	def create_player(self):
		self.player = Player(random.choice(self.spawn_points),self)

	def create_NPC(self):
		NPC(random.choice(self.spawn_points),self)
		self.createNPC_time = pygame.time.get_ticks()

	def cooldown_create_NPC(self):
		current_time = pygame.time.get_ticks()
		if NPC.Amount < 10 and current_time - self.createNPC_time >= CREATE_NPC_DURATION:
			self.create_NPC()

	def run(self, delta_time):	
		self.cooldown_create_NPC()
		
		for object in self.visible_sprites:
			object.before_update(delta_time)
			object.update(delta_time)
			object.after_update()

		self.minimap.update()
		
		self.visible_sprites.draw(self.player)

		self.minimap.draw()

class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self, level):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		
		self.level = level

		# offset dùng để duy chuyển camera 
		self.offset = pygame.math.Vector2()
		
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2

	def draw(self, target):
		self.offset.x = target.rect.centerx - self.half_width
		self.offset.y = target.rect.centery - self.half_height

<<<<<<< HEAD
		self.display_surface.blit(self.level.map_ground_image, - self.offset)

=======
		self.display_surface.blit(self.level.map_ground_image, -self.offset)
		
>>>>>>> 03df69a03265a2e25cdfdb1e5a8f867c9fae577d
		for sprite in sorted(self.sprites(),key= lambda sprite: sprite.hitbox.centery):
				sprite.render(self.offset)

