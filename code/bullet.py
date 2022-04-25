import math
import pygame

class Bullet(pygame.sprite.Sprite):
	def __init__(self, player, groups):
		super().__init__(groups)
		self.image = pygame.image.load("../graphics/test/BulletProjectile.png").convert_alpha()
		angle = player.angle
		self.image = pygame.transform.rotate(self.image,-angle)
		self.rect = self.image.get_rect(center= player.rect.center)
		#movement
		angle = math.radians(angle)
		self.speed_x = 6*math.cos(angle)
		self.speed_y = 6*math.sin(angle)

	def collision(self, direction):
		pass


	def update(self):
		self.rect.x += self.speed_x
		self.rect.y += self.speed_y

		