import pygame
from bullet import Bullet
from game_object import GameObject
from utils import Utils
from settings import *
from math import atan2,degrees


class Player(GameObject):
	def __init__(self, pos, Level):
		self.level =  Level
		self.visible_sprites = Level.visible_sprites
		self.obstacle_sprites = Level.obstacle_sprites
		
		super().__init__([Level.visible_sprites, Level.player_sprites], 'graphics/test/player.png', pos, (-2, -13))
		self.bullet_sprites = Level.bullet_sprites


		#movement
		self.direction = pygame.math.Vector2(0,0)
		self.speed = 5
		self.angle = 0
		self.attacking = False
		self.attack_cooldown = 400
		self.attack_time = None
		self.stunt_count_down = 0
		self.prev_stunt_time = 0

		#rotate
		self.original_image = self.image

	def input(self):
		keys_press = pygame.key.get_pressed()
		if keys_press[pygame.K_w]:
			self.direction.y = -1
		elif keys_press[pygame.K_s]:
			self.direction.y = 1
		else:
			self.direction.y = 0

		if keys_press[pygame.K_d]:
			self.direction.x = 1
		elif keys_press[pygame.K_a]:
			self.direction.x = -1
		else:
			self.direction.x = 0
		
		left_mouse_pressed = pygame.mouse.get_pressed()[0]
		if left_mouse_pressed and not self.attacking:
			self.attacking = True 
			self.attack_time = pygame.time.get_ticks()
			self.shoot()	

	def shoot(self):
		Bullet(self,self.level)

	def collision_horizontal(self):
		for sprite in self.obstacle_sprites:
			if sprite.hitbox.colliderect(self.hitbox):
				if self.direction.x > 0:  # moving right
					self.hitbox.right = sprite.hitbox.left
					
				elif self.direction.x < 0:  # moving left
					self.hitbox.left = sprite.hitbox.right
		
	def collision_vertical(self):
		for sprite in self.level.obstacle_sprites:
			if sprite.hitbox.colliderect(self.hitbox):
				if self.direction.y > 0:  # moving down
					self.hitbox.bottom = sprite.hitbox.top
				elif self.direction.y < 0:  # moving up
					self.hitbox.top = sprite.hitbox.bottom

	def cooldown(self):
		current_time = pygame.time.get_ticks()

		if self.attacking:
			if current_time - self.attack_time >= self.attack_cooldown:
				self.attacking = False

	def stunted(self):
		self.prev_stunt_time = pygame.time.get_ticks()
		self.stunt_count_down = PLAYER_STUNT_DURATION
		self.direction = pygame.math.Vector2()

	def update(self):

		if (self.stunt_count_down <= 0):
			self.input()	
		else:
			self.stunt_count_down -= pygame.time.get_ticks() - self.prev_stunt_time
			self.prev_stunt_time = pygame.time.get_ticks() 
		
		self.cooldown()
		Utils.move(self, self.speed)

		mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())
		mouse_pos += self.level.visible_sprites.offset

		Utils.face_toward(self,mouse_pos)