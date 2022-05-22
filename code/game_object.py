from assets import Assets
from utils import Utils 
import pygame

class GameObject(pygame.sprite.Sprite):
	def __init__(self, level, group, image=None, hitbox_inflation=(0, 0), pos=(0, 0), _direction=pygame.math.Vector2(), speed=0):
		'''make the game object'''
		if image is None:
			image = Assets.player1.down_idle[0]
		
		group.append(level.group_all)
		super().__init__(group)
		self._level = level
		self._direction = _direction
		self._speed = speed
		self._vel = _direction * 0

		self.image = image
		self._rect = self.image.get_rect(topleft=pos)
		self._hitbox = self._rect.inflate(*hitbox_inflation)

	@property
	def rect(self):
		return self._rect

	@property
	def hitbox(self):
		return self._hitbox

	@property
	def vel(self):
		return self._vel

	def render(self, camera):
		'''render object in camera
		param camera: surface of camera
		'''
		camera.surface.blit(self.image, camera.apply(self))

	def before_update(self, delta_time):
		'''update the velocity affter FPS
		param delta_time: FPS'''
		self._vel = self._direction * (self._speed * delta_time)

	def update(self, delta_time):
		pass

	def after_update(self):
		'''update pos of objects'''
		vel_x, vel_y = Utils.round_away_from_zero(self._vel.x), Utils.round_away_from_zero(self._vel.y)
		self._hitbox.x += vel_x
		self._hitbox.y += vel_y

		self._rect.x += vel_x
		self._rect.y += vel_y
	

