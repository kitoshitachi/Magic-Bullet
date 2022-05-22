from dataclasses import dataclass
import pygame
from bullet import Bullet
from clock import Countdown
from assets import MovingImages, Assets
from sprite_animation import SpriteAnimation
from collision import CollisionEngine, CollisionResponse
from game_object import GameObject
from settings import *

@dataclass
class KeySettings:
	'''make class save setting keyboard'''
	left: int
	right: int
	up: int
	down: int
	rotate_left: int
	rotate_right: int
	shoot: int
	run:int

class Player(GameObject):
	def __init__(self, pos, level, key_settings:KeySettings, player_asset: MovingImages):	
		'''
		make player
		param pos: start pos
		param level: get attribute level
		keysetting: the setting of player
		player_asset: get all assets of player
		'''	
		super().__init__(
			level=level,
			group=[level.group_visible, level.group_player],
	  		hitbox_inflation=(-6, -32),
			pos=pos,
			_direction=pygame.math.Vector2(0, 0),
			speed=PLAYER_SPEED
		)
		self._hitbox.center = (self._rect.centerx, self._rect.centery + 14)
		self.mp = PLAYER_MANA
		self.stamina = PLAYER_STAMINA
		
		self.attack_timer = Countdown(ATTACK_COOLDOWN)
		self.regen_timer = Countdown(REGEN_COOLDOWN)
		self.stunt_timer = Countdown(STUNT_DURATION)

		self.key_settings = key_settings
		#movement
		self.rot_direction = 0
		self.angle = 0
		self.player_asset = player_asset
		self._animation = SpriteAnimation(self, self.player_asset.down_idle, 8)
		self.sprite_angle = 90
		self.circle_rect = Assets.circle.get_rect(center=self._rect.center)
		self.arrow_img = Assets.arrow
		self.arrow_rect = Assets.arrow.get_rect(center=self._rect.center)
		self.arrow_push_vector = pygame.math.Vector2(self.circle_rect.width // 2, 0)

	def input(self):
		'''handle input'''
		ks = self.key_settings
		keys_press = pygame.key.get_pressed()
		
		if keys_press[ks.rotate_right]:
				self.rot_direction = 1
		elif keys_press[ks.rotate_left]:
				self.rot_direction = -1
		else:
			self.rot_direction = 0

		if keys_press[ks.up]:
			self._direction.y = -1
		elif keys_press[ks.down]:
			self._direction.y = 1
		else:
			self._direction.y = 0

		if keys_press[ks.run] and self.stamina >= 60:
			self._speed = PLAYER_SPEED * 1.6
			self.stamina -= 60
		else:
			self._speed = PLAYER_SPEED

		if keys_press[ks.right]:
			self._direction.x = 1
		elif keys_press[ks.left]:
			self._direction.x = -1
		else:
			self._direction.x = 0

		if self._direction.magnitude() != 0:
			self._direction.normalize_ip()
		
		if self.attack_timer.is_done and self.mp >= 20:    
			if keys_press[ks.shoot]:
				self.shoot()	
				
	def shoot(self):
		'''take a shoot'''
		self.mp -= 20
		Bullet(self,self._level)
		self.attack_timer.reset()
	def handle_collision(self):
		'''check collision sweet AABB, respone slide'''
		CollisionEngine.detect_multiple(self, self._level.obstacles_and_boundary, CollisionResponse.slide)

	def stunted(self):
		'''stunt player'''
		self.stunt_timer.reset()
		self._direction.x, self._direction.y = 0, 0
		self.rot_direction = 0

	def npc_collision(self):
		'''handle collision npc'''

		hits = pygame.sprite.spritecollide(self,self._level.group_NPC,False,lambda one,two: one.hitbox.colliderect(two.hitbox))
		for npc in hits:
			mana = 2
			self.regen_timer.reset()
			if self.mp < mana:
				npc.mp += self.mp
				self.mp = 0
			else:
				self.mp -= mana
				npc.mp += mana

	def update(self, delta_time):
		'''update player at this FPS'''
		if self.stunt_timer.is_done:
			self.input()	
		if self.regen_timer.is_done and self.mp < PLAYER_MANA:
			self.mp += 2
			self.regen_timer.reset()
		if self.stamina < PLAYER_STAMINA:
			self.stamina += 1 

		self.handle_collision()
		self.npc_collision()
		self.update_rotation(delta_time)
		self.update_animation(delta_time)
		if self.mp < 0:
			self.mp = 0
		if self.mp >= PLAYER_MANA:
			self.mp = PLAYER_MANA
		

	def update_animation(self, delta_time):
		'''update animation at this FPS'''
		if self._direction.x == 0 and self._direction.y == 0:
			self._animation.set_images(self.player_asset.idle_sequence(self.angle), reset=False)
			self._animation.animation_speed = 1
		else:
			self.sprite_angle = pygame.Vector2(1, 0).angle_to(self._direction)
			self._animation.set_images(self.player_asset.move_squence(self.angle), reset=False)
			self._animation.animation_speed = 8

		self._animation.update(delta_time)

	def update_rotation(self, delta_time):
		'''update angle of player at this FPS'''
		self.angle = (self.angle + self.rot_direction * PLAYER_ROT_SPEED * delta_time) % 360

	def after_update(self):
		'''update the arrow'''
		super().after_update()
		self.circle_rect.center = self._rect.center

		self.arrow_push_vector = pygame.Vector2(self.circle_rect.width // 2, 0).rotate(self.angle)
		self.arrow_img = pygame.transform.rotate(Assets.arrow, -self.angle)

		self.arrow_rect.center = self._rect.center
		self.arrow_rect.x += self.arrow_push_vector.x
		self.arrow_rect.y += self.arrow_push_vector.y


	def render(self, camera):
		'''
		render player in camera
		param camera: the camera of player
		'''
		super().render(camera)
		camera.surface.blit(Assets.circle, camera.apply_rect(self.circle_rect))
		camera.surface.blit(self.arrow_img, camera.apply_rect(self.arrow_rect))

class Player1(Player):
	'''
	subclass to make player 1 difference keysetting
	'''
	def __init__(self, pos, level):
		super().__init__(pos, level, KeySettings(pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_g, pygame.K_j, pygame.K_h,pygame.K_LSHIFT), Assets.player1)

class Player2(Player):
	'''
	subclass to make player 1 difference keysetting
	'''
	def __init__(self, pos, level):
		super().__init__(pos, level, KeySettings(pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_i, pygame.K_p, pygame.K_o,pygame.K_u), Assets.player2)
