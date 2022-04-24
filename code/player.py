import pygame
from pyparsing import original_text_for
from settings import *
from math import atan2,degrees,isclose

class Player(pygame.sprite.Sprite):
	def __init__(self, pos, groups,visible_sprites, obstacle_sprites):
		super().__init__(groups)
		self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
		self.rect = self.image.get_rect(topleft=pos)
		self.visible_sprites = visible_sprites
		self.obstacle_sprites = obstacle_sprites
		self.direction = pygame.math.Vector2()
		self.speed = 5
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
		
		
	def rotate_player(self):
		mx,my = pygame.mouse.get_pos()
		original_rect = self.rect
		dx, dy = mx - original_rect.centerx + self.visible_sprites.offset.x , my - original_rect.centery + self.visible_sprites.offset.y
		angle = degrees(atan2(dy, dx))
		self.image = pygame.transform.rotate(self.original_image, -angle)
		self.rect = self.image.get_rect(center=original_rect.center)

	def move(self, run_speed):
		previous_pos = self.rect.copy()
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()

		self.rect.x += self.direction.x * run_speed
		self.rect.y += self.direction.y * run_speed
		self.collision(previous_pos)
		
	def collision(self,pos):
		for sprite in self.obstacle_sprites:
			if sprite.rect.colliderect(self.rect):
				if isclose(sprite.rect.right, self.rect.left, abs_tol=2) or isclose(sprite.rect.left, self.rect.right, abs_tol=2):
					self.rect.x = pos.x
				elif isclose(sprite.rect.top, self.rect.bottom, abs_tol=2) or isclose(sprite.rect.bottom, self.rect.top, abs_tol=2):
					self.rect.y = pos.y
				else:
					self.rect.x = pos.x
					self.rect.y = pos.y

	def update(self):
		self.input()
		self.move(self.speed)
		self.rotate_player()