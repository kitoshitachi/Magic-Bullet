import pygame

from settings import MINIMAP_TILE_SIZE, TILESIZE

class Minimap(pygame.sprite.Sprite):
	def __init__(self, pos, player, minimap_image):
		super().__init__()
		self.image = pygame.image.load('graphics/test/rock.png').convert_alpha()
		self.pos = pos
		self.player = player

		self.minimap_image = minimap_image
		self.player_surface = pygame.Surface(minimap_image.get_size(), pygame.SRCALPHA)
		
		self.display_surface = pygame.display.get_surface()

	def update(self):
		self.player_surface.fill((0, 0, 0, 0))

		x = self.player.rect.topleft[0] / TILESIZE
		y = self.player.rect.topleft[1] / TILESIZE
		pygame.draw.rect(self.player_surface, (255, 0, 0), pygame.Rect(
			x * MINIMAP_TILE_SIZE, y * MINIMAP_TILE_SIZE, MINIMAP_TILE_SIZE, MINIMAP_TILE_SIZE))

	def draw(self):
		self.display_surface.blit(self.minimap_image, self.pos)
		self.display_surface.blit(self.player_surface, self.pos)
