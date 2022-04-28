import itertools
import pygame
from utils import Utils
from settings import BULLET_MAX_TIME_TO_LIVE
from debug import debug

class Bullet(pygame.sprite.Sprite):
	def __init__(self,player,Level):
		self.owner = player
		self.level = Level
		self.obstacle_sprites = Level.obstacle_sprites
		self.bullet_sprites = Level.bullet_sprites
		self.player_sprites = Level.player_sprites
		super().__init__(Level.visible_sprites,self.bullet_sprites)
		self.image = pygame.image.load("../graphics/test/BulletProjectile.png").convert_alpha()
		
		self.image = pygame.transform.rotate(self.image,-player.angle)
		self.rect = self.image.get_rect(topleft = player.rect.topleft)
		self.hitbox = self.rect.inflate(0,0)

		#movement
		self.direction = pygame.math.Vector2(1,0).rotate(player.angle)
		self.speed = 12
		self.time_to_live = BULLET_MAX_TIME_TO_LIVE

	def collision_horizontal(self):
		for sprite in itertools.chain(self.bullet_sprites, self.obstacle_sprites):
			if sprite is self:
				continue

			if sprite.hitbox.colliderect(self.hitbox):
				self.time_to_live -= 1
				if self.direction.x > 0:  # moving right
					self.hitbox.right = sprite.hitbox.left
					self.direction.reflect_ip(pygame.math.Vector2(-1,0))

				elif self.direction.x < 0:  # moving left
					self.hitbox.left = sprite.hitbox.right
					self.direction.reflect_ip(pygame.math.Vector2(1,0))

	def collision_vertical(self):
		for sprite in itertools.chain(self.bullet_sprites, self.obstacle_sprites):
			if sprite is self:
				continue	

			if sprite.hitbox.colliderect(self.hitbox):
				self.time_to_live -= 1
				if self.direction.y > 0:  # moving down
					self.hitbox.bottom = sprite.hitbox.top
					self.direction.reflect_ip(pygame.math.Vector2(0,1))
				elif self.direction.y < 0:  # moving up
					self.hitbox.top = sprite.hitbox.bottom
					self.direction.reflect_ip(pygame.math.Vector2(0,-1))

	def player_collision(self):
		for player in pygame.sprite.spritecollide(self,self.player_sprites,False):
			if player is not self.owner or self.time_to_live != BULLET_MAX_TIME_TO_LIVE:
				self.stunt_count_down = 500
				player.stunted()

	def update(self):
		Utils.move(self,self.speed)
		self.player_collision()

		if self.time_to_live == 0:
			self.kill()


		