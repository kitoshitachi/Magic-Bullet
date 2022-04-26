from math import cos, radians, sin
from numpy import angle
import pygame
from player import Player
from wall import Wall

from debug import debug
class Bullet(pygame.sprite.Sprite):
	def __init__(self, player:Player, groups):
		super().__init__(groups)
		self.image = pygame.image.load("../graphics/weapons/lance/full.png").convert_alpha()
		self.image = pygame.transform.rotate(self.image,-player.angle)
		self.rect = self.image.get_rect(topleft = player.rect.topleft)
		self.hitbox = self.rect.inflate(0,0)

		self.player_groups = player.groups().copy()
		self.obstacle_groups = player.visible_sprites.copy()

		self.direction = pygame.math.Vector2(1,0).rotate(player.angle)
		self.speed = 8
		self.time_to_live = 3

	def collision_horizontal(self):
		for sprite in pygame.sprite.spritecollide(self,self.obstacle_groups,False):
			if self.direction.x > 0:  # moving right
				self.hitbox.right = sprite.hitbox.left
				self.direction.reflect_ip(pygame.math.Vector2(-1,0))

			elif self.direction.x < 0:  # moving left
				self.hitbox.left = sprite.hitbox.right
				self.direction.reflect_ip(pygame.math.Vector2(1,0))


	def collision_vertical(self):
		for sprite in pygame.sprite.spritecollide(self,self.obstacle_groups,False):
			if self.direction.y > 0:  # moving down
				self.hitbox.bottom = sprite.hitbox.top
				self.direction.reflect_ip(pygame.math.Vector2(0,1))

			elif self.direction.y < 0:  # moving up
				self.hitbox.top = sprite.hitbox.bottom
				self.direction.reflect_ip(pygame.math.Vector2(0,-1))

	def collision_other_player(self):
		pygame.sprite.groupcollide(self.groups(),self.player_groups,True,True)

	def move(self,speed):
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()

		self.hitbox.x += self.direction.x * speed
		self.collision_horizontal()
		
		self.hitbox.y += self.direction.y * speed
		self.collision_vertical()	
		
		self.rect.center = self.hitbox.center

	def update(self):
		Player.move(self)
		if self.time_to_live == 0:
			self.kill()


		