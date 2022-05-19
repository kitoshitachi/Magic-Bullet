from dataclasses import dataclass
import itertools
import pygame
from bullet import Bullet
from assets import Assets
from clock import Countdown
from sprite_animation import SpriteAnimation
from collision import CollisionEngine, CollisionResponse
from game_object import GameObject
from settings import *
@dataclass
class KeySettings:
	left: int
	right: int
	up: int
	down: int
	rotate_left: int
	rotate_right: int
	shoot: int
	run:int

class Player(GameObject):
	def __init__(self, pos, level, key_settings:KeySettings):		
		super().__init__(
			level=level,
			group=[level.group_visible, level.group_player],
	  		hitbox_inflation=(-6, -32),
			pos=pos,
			direction=pygame.math.Vector2(0, 0),
			speed=PLAYER_SPEED
		)
		self.hitbox.center = (self.rect.centerx, self.rect.centery + 14)
		self.mp = PLAYER_MANA
		self.stamina = PLAYER_STAMINA
		
		self.attack_timer = Countdown(ATTACK_COOLDOWN)
		self.regen_timer = Countdown(REGEN_COOLDOWN)
		self.stunt_timer = Countdown(STUNT_DURATION)

		self.group_visible = level.group_visible
		self.group_obstacle = level.group_obstacle
		self.group_bullet = level.group_bullet

		self.key_settings = key_settings
		#movement
		self.rot_direction = 0
		self.angle = 0
		self.animation = SpriteAnimation(self, Assets.player1.down_idle, 8)
		self.sprite_angle = 90
		self.circle_rect = Assets.circle.get_rect(center=self.rect.center)
		self.arrow_img = Assets.arrow
		self.arrow_rect = Assets.arrow.get_rect(center=self.rect.center)
		self.arrow_push_vector = pygame.math.Vector2(self.circle_rect.width // 2, 0)

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

		if keys_press[ks.run] and self.stamina >= 60:
			self.speed = PLAYER_SPEED * 1.6
			self.stamina -= 60
		else:
			self.speed = PLAYER_SPEED

		if keys_press[ks.right]:
			self.direction.x = 1
		elif keys_press[ks.left]:
			self.direction.x = -1
		else:
			self.direction.x = 0

		if self.direction.magnitude() != 0:
			self.direction.normalize_ip()
		
		if self.attack_timer.is_done and self.mp >= 20:    
			if keys_press[ks.shoot]:
				self.shoot()	
				
	def shoot(self):
		self.mp -= 20
		Bullet(self,self.level)
		self.attack_timer.reset()
	def handle_collision(self):
		obstacles_and_boundary = itertools.chain(self.level.group_obstacle, self.level.group_boundary)
		CollisionEngine.detect_multiple(self, obstacles_and_boundary, CollisionResponse.slide)
	
	def stunted(self):
		self.stunt_timer.reset()
		self.direction.x, self.direction.y = 0, 0
		self.rot_direction = 0

	def update(self, delta_time):
		if self.stunt_timer.is_done:
			self.input()	
		if self.regen_timer.is_done and self.mp < PLAYER_MANA:
			self.mp += 2
			self.regen_timer.reset()
		if self.stamina < PLAYER_STAMINA:
			self.stamina += 1 

		self.handle_collision()
		self.update_rotation(delta_time)
		self.update_animation(delta_time)

	def update_animation(self, delta_time):
		if self.direction.x == 0 and self.direction.y == 0:
			self.animation.set_images(Assets.player1.get_idle_sequence_from_angle(self.angle), reset=False)
			self.animation.set_animation_speed(1)
		else:
			self.sprite_angle = pygame.Vector2(1, 0).angle_to(self.direction)
			self.animation.set_images(Assets.player1.get_move_sequence_from_angle(self.angle), reset=False)
			self.animation.set_animation_speed(8)

		self.animation.update(delta_time)

	def update_rotation(self, delta_time):
		self.angle = (self.angle + self.rot_direction * PLAYER_ROT_SPEED * delta_time) % 360

	def after_update(self):
		super().after_update()
		self.circle_rect.center = self.rect.center

		self.arrow_push_vector = pygame.Vector2(self.circle_rect.width // 2, 0).rotate(self.angle)
		self.arrow_img = pygame.transform.rotate(Assets.arrow, -self.angle)

		self.arrow_rect.center = self.rect.center
		self.arrow_rect.x += self.arrow_push_vector.x
		self.arrow_rect.y += self.arrow_push_vector.y


	def render(self, camera):
		super().render(camera)
		camera.surface.blit(Assets.circle, camera.apply_rect(self.circle_rect))
		camera.surface.blit(self.arrow_img, camera.apply_rect(self.arrow_rect))

@dataclass
class KeySettings:
	left: int
	right: int
	up: int
	down: int
	rotate_left: int
	rotate_right: int
	shoot: int
	run: int

class Player1(Player):
	def __init__(self, pos, level):
		super().__init__(pos, level, KeySettings(pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_g, pygame.K_j, pygame.K_h,pygame.K_LSHIFT))

class Player2(Player):
	def __init__(self, pos, level):
		super().__init__(pos, level, KeySettings(pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_i, pygame.K_p, pygame.K_o,pygame.K_u))
