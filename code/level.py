import pygame
from settings import *
from minimap import Minimap 
from wall import Wall
from player import Player
from bullet import Bullet
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
		# sprite setup
		self.create_map()
		# others
		self.minimap = Minimap((16, 16), self.player)

	def create_map(self):
		for row_index,row in enumerate(WORLD_MAP):
			for col_index, col in enumerate(row):
				x = col_index * TILESIZE
				y = row_index * TILESIZE
				if col == 'x':
					Wall((x,y),[self.visible_sprites,self.obstacle_sprites])
				if col == 'p':
					self.player = Player((x,y),self)

	def run(self):
		# update and draw the game
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
