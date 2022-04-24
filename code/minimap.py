from turtle import pos
import pygame
from settings import *

class Minimap(pygame.sprite.Sprite):
	def __init__(self, pos, player):
		super().__init__()
		self.image = pygame.image.load('../graphics/test/rock.png').convert_alpha()
		self.pos = pos
		self.player = player

		self.minimap_surface = pygame.Surface((len(WORLD_MAP[0]) * MINIMAP_TILE_SIZE, len(WORLD_MAP) * MINIMAP_TILE_SIZE))
		self.minimap_surface.fill((0, 0, 0))
		self.player_surface = pygame.Surface((len(WORLD_MAP[0]) * MINIMAP_TILE_SIZE, len(WORLD_MAP) * MINIMAP_TILE_SIZE), pygame.SRCALPHA)
		
		self.display_surface = pygame.display.get_surface()

		for y, row in enumerate(WORLD_MAP):
			for x, col in enumerate(row):
				if col == 'x':
					pygame.draw.rect(self.minimap_surface, (255, 255, 255), pygame.Rect(
						x * MINIMAP_TILE_SIZE, y * MINIMAP_TILE_SIZE, MINIMAP_TILE_SIZE, MINIMAP_TILE_SIZE))

	def update(self):
		self.player_surface.fill((0, 0, 0, 0))

		x = self.player.rect.topleft[0] / TILESIZE
		y = self.player.rect.topleft[1] / TILESIZE
		pygame.draw.rect(self.player_surface, (255, 0, 0), pygame.Rect(
			x * MINIMAP_TILE_SIZE, y * MINIMAP_TILE_SIZE, MINIMAP_TILE_SIZE, MINIMAP_TILE_SIZE))

	def draw(self):
		self.display_surface.blit(self.minimap_surface, self.pos)
		self.display_surface.blit(self.player_surface, self.pos)
