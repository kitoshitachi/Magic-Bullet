from dataclasses import dataclass
import itertools
import pygame
from bullet import Bullet
from assets import Assets
from clock import Countdown
from collision import CollisionEngine, CollisionResponse
from game_object import GameObject
from settings import *

class Player(GameObject):
	def __init__(self, pos, level, key_settings):		
		super().__init__(
			level=level,
			group=[level.group_visible, level.group_player],
			image=Assets.player,
			hitbox_inflation=(-6, -13),
			pos=pos,
			direction=pygame.math.Vector2(0, 0),
			speed=300)
		self.mp = PLAYER_MANA
		self.attack_timer = Countdown(ATTACK_COOLDOWN)
		self.stunt_timer = Countdown(STUNT_DURATION)
		self.group_visible = level.group_visible
		self.group_obstacle = level.group_obstacle
		self.group_bullet = level.group_bullet
		self.key_settings = key_settings

		#movement
		self.rot_direction = 0
		self.angle = 0

		#rotate
		self.original_image = self.image

	def input(self):
		ks = self.key_settings
		keys_press = pygame.key.get_pressed()
		
		if keys_press[ks.rotate_right]:
				self.rot_direction = 1
		elif keys_press[ks.rotate_left]:
				self.rot_direction = -1
		else:
			self.rot_direction = 0

		if keys_press[ks.up]:
			self.direction.y = -1
		elif keys_press[ks.down]:
			self.direction.y = 1
		else:
			self.direction.y = 0

		if keys_press[ks.right]:
			self.direction.x = 1
		elif keys_press[ks.left]:
			self.direction.x = -1
		else:
			self.direction.x = 0

		if self.direction.magnitude() != 0:
			self.direction.normalize_ip()
		
		if self.attack_timer.is_done:    
			if keys_press[ks.shoot]:
				self.shoot()	
				self.attack_timer.reset()

	def shoot(self):
		Bullet(self,self.level)

	def handle_collision(self):
			obstacles_and_boundary = itertools.chain(self.level.group_obstacle, self.level.group_boundary)
			CollisionEngine.detect_multiple(self, obstacles_and_boundary, CollisionResponse.slide)
		
	def stunted(self):
		self.stunt_timer.reset()
		self.direction.x,self.direction.y = 0,0 

	def rotate(self, delta_time):
		self.angle = (self.angle + self.rot_direction * PLAYER_ROT_SPEED * delta_time) % 360
		self.image = pygame.transform.rotate(Assets.player, -self.angle)
		self.rect = self.image.get_rect(center = self.rect.center)

	def update(self, delta_time):
		if self.stunt_timer.is_done:
			self.input()	
		
		self.rotate(delta_time)
		self.handle_collision()

@dataclass
class KeySettings:
		left: int
		right: int
		up: int
		down: int
		rotate_left: int
		rotate_right: int
		shoot: int

class Player1(Player):
	def __init__(self, pos, level):
			super().__init__(pos, level, KeySettings(pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_g, pygame.K_j, pygame.K_h))

class Player2(Player):
	def __init__(self, pos, level):
			super().__init__(pos, level, KeySettings(pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_i, pygame.K_p, pygame.K_o))
