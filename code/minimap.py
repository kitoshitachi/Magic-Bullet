import pygame

from settings import MINIMAP_TILE_SIZE, TILESIZE

class Minimap(pygame.sprite.Sprite):
	def __init__(self, pos, players, minimap_image):
		super().__init__()
		self.image = pygame.image.load('graphics/test/rock.png').convert_alpha()
		self.pos = pos
		self.players = players

		self.minimap_image = minimap_image
		self.players_surface = pygame.Surface(minimap_image.get_size(), pygame.SRCALPHA)
		
		self.display_surface = pygame.display.get_surface()

	def update(self):
		self.players_surface.fill((0, 0, 0, 0))
		for player in self.players:
			x, y = player.rect.x / TILESIZE, player.rect.y / TILESIZE
			pygame.draw.rect(self.players_surface, (255, 0, 0), pygame.Rect(x * MINIMAP_TILE_SIZE, y * MINIMAP_TILE_SIZE, MINIMAP_TILE_SIZE, MINIMAP_TILE_SIZE))

	def draw(self):
		self.display_surface.blit(self.minimap_image, self.pos)
		self.display_surface.blit(self.players_surface, self.pos)
