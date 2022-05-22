from assets import Assets
from utils import Utils 
import pygame

class GameObject(pygame.sprite.Sprite):
	def __init__(self, level, group, image=None, hitbox_inflation=(0, 0), pos=(0, 0), direction=pygame.math.Vector2(), speed=0):
		'''make the game object'''
		if image is None:
			image = Assets.player1.down_idle[0]
		
		group.append(level.group_all)
		super().__init__(group)
		self.level = level
		self.direction = direction
		self.speed = speed
		self.vel = direction * 0

		self.image = image
		self.rect = self.image.get_rect(topleft=pos)
		self.hitbox = self.rect.inflate(*hitbox_inflation)
		
	def render(self, camera):
		'''render object in camera
		param camera: surface of camera
		'''
		camera.surface.blit(self.image, camera.apply(self))

	def before_update(self, delta_time):
		'''update the velocity at this FPS
		param delta_time: FPS'''
		self.vel = self.direction * (self.speed * delta_time)

	def update(self, delta_time):
		pass

	def after_update(self):
		'''update pos of objects'''
		vel_x, vel_y = Utils.round_away_from_zero(self.vel.x), Utils.round_away_from_zero(self.vel.y)
		self.hitbox.x += vel_x
		self.hitbox.y += vel_y

		self.rect.x += vel_x
		self.rect.y += vel_y
	

