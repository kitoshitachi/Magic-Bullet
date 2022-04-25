import pygame
from settings import *
from math import atan2,degrees
from bullet import Bullet
class Player(pygame.sprite.Sprite):
	def __init__(self, pos, groups, visible_sprites, obstacle_sprites,create_bullet):
		super().__init__(groups)
		self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
		self.rect = self.image.get_rect(topleft=pos)
		self.hitbox = self.rect.inflate(0,-26)

		self.visible_sprites = visible_sprites
		self.obstacle_sprites = obstacle_sprites

		#movement
		self.direction = pygame.math.Vector2()
		self.speed = 5
		self.attacking = False
		self.attack_cooldown = 400
		self.attack_time = None
		self.angle = 0
		self.create_bullet = create_bullet
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

		if keys_press[pygame.K_SPACE] and not self.attacking:
			self.attacking = True 
			self.attack_time = pygame.time.get_ticks()
			self.create_bullet()
		
		
	def rotate_player(self):
		mx,my = pygame.mouse.get_pos()
		original_rect = self.rect
		dx, dy = mx - original_rect.centerx + self.visible_sprites.offset.x , my - original_rect.centery + self.visible_sprites.offset.y
		self.angle = degrees(atan2(dy, dx))
		self.image = pygame.transform.rotate(self.original_image, -self.angle)
		self.rect = self.image.get_rect(center=original_rect.center)

	def move(self, speed):
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()

		self.hitbox.x += self.direction.x * speed
		self.collision('horizontal')
		self.hitbox.y += self.direction.y * speed
		self.collision('vertical')
		self.rect.center = self.hitbox.center

	def shoot(self):
		bullet = Bullet(self.rect,self.angle)
		

	def collision(self, direction):
		if direction == 'horizontal':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.x > 0:  # moving right
						self.hitbox.right = sprite.hitbox.left
					if self.direction.x < 0:  # moving left
						self.hitbox.left = sprite.hitbox.right

		if direction == 'vertical':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.y > 0: # moving down
						self.hitbox.bottom = sprite.hitbox.top
					if self.direction.y < 0: # moving up
						self.hitbox.top = sprite.hitbox.bottom

	def cooldown(self):
		current_time = pygame.time.get_ticks()

		if self.attacking:
			if current_time - self.attack_time >= self.attack_cooldown:
				self.attacking = False

	def update(self):
		self.input()
		self.cooldown()
		
		self.move(self.speed)
		self.rotate_player()