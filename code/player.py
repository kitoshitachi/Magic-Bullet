import pygame
from pyparsing import original_text_for
from settings import *
from math import atan2,degrees,pi

class Player(pygame.sprite.Sprite):
	def __init__(self, pos, groups,visible_sprites, obstacle_sprites):
		super().__init__(groups)
		self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
		self.rect = self.image.get_rect(topleft=pos)
		self.obstacle_sprites = obstacle_sprites
		self.direction = pygame.math.Vector2()
		self.speed = 5
		self.original_image = self.image
		self.visible_sprites = visible_sprites

	def input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_w]:
			self.direction.y = -1
		elif keys[pygame.K_s]:
			self.direction.y = 1
		else:
			self.direction.y = 0

		if keys[pygame.K_d]:
			self.direction.x = 1
		elif keys[pygame.K_a]:
			self.direction.x = -1
		else:
			self.direction.x = 0
		
	def rotate_player(self):
		mx,my = pygame.mouse.get_pos()
		original_rect = self.rect
		dx, dy = mx - original_rect.centerx + self.visible_sprites.offset.x , my - original_rect.centery + self.visible_sprites.offset.y
		angle = (180 / pi) * - atan2(dy, dx) 
		self.image = pygame.transform.rotate(self.original_image, int(angle))
		self.rect = self.image.get_rect(center=original_rect.center)

	def move(self, speed):
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()

		self.rect.x += self.direction.x * speed
		self.collision('horizontal')
		self.rect.y += self.direction.y * speed
		self.collision('vertical')

	def collision(self, direction):
		if direction == 'horizontal':
			for sprite in self.obstacle_sprites:
				if sprite.rect.colliderect(self.rect):
					if self.direction.x > 0:  # moving right
						self.rect.right = sprite.rect.left
					if self.direction.x < 0:  # moving left
						self.rect.left = sprite.rect.right

		if direction == 'vertical':
			for sprite in self.obstacle_sprites:
				if sprite.rect.colliderect(self.rect):
					if self.direction.y > 0: # moving down
						self.rect.bottom = sprite.rect.top
					if self.direction.y < 0: # moving up
						self.rect.top = sprite.rect.bottom
	
	def update(self):
		self.input()
		self.move(self.speed)
		self.rotate_player()