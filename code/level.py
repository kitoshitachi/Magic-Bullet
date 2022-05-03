import random
import pygame
from NPC import NPC
from settings import TILESIZE, WORLD_MAP, CREATE_NPC_DURATION
from minimap import Minimap 
from wall import Wall
from player import Player
from debug import debug

class Level:
	def __init__(self):

		# get the display surface 
		self.display_surface = pygame.display.get_surface()

		# sprite group setup
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()
		self.bullet_sprites = pygame.sprite.Group()
		self.player_sprites = pygame.sprite.Group()
		self.NPC_sprites = pygame.sprite.Group()
		# sprite setup
		self.No_sprites = []
		self.create_map()
		self.create_player()
		self.create_NPC()
		# others
		self.minimap = Minimap((16, 16), self.player)

		self.createNPC_time = 0


	def create_map(self):
		for row_index,row in enumerate(WORLD_MAP):
			for col_index, col in enumerate(row):
				x = col_index * TILESIZE
				y = row_index * TILESIZE
				if col == 'x':
					Wall((x,y),[self.visible_sprites,self.obstacle_sprites])
				if col == ' ':
					self.No_sprites.append((x,y))
					

	def create_player(self):
		self.player = Player(random.choice(self.No_sprites),self)

	def create_NPC(self):
		NPC(random.choice(self.No_sprites),self)
		self.createNPC_time = pygame.time.get_ticks()

	def cooldown_create_NPC(self):
		current_time = pygame.time.get_ticks()
		if NPC.Amount < 10 and current_time - self.createNPC_time >= CREATE_NPC_DURATION:
			self.create_NPC()

	def run(self):	
		self.cooldown_create_NPC()
		self.visible_sprites.update()
		self.minimap.update()
		
		self.visible_sprites.draw(self.player)

		self.minimap.draw()

class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		
		# offset dùng để duy chuyển camera 
		self.offset = pygame.math.Vector2()
		
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2

	def draw(self, target):
		for sprite in sorted(self.sprites(),key= lambda sprite: sprite.rect.centery):
			self.offset.x = target.rect.centerx - self.half_width
			self.offset.y = target.rect.centery - self.half_height

			self.display_surface.blit(sprite.image, sprite.rect.topleft - self.offset)
