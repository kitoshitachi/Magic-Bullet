import pygame
from game_object import GameObject
from settings import *

class Obstacle(GameObject):
	def __init__(self, image, area, pos, hitbox, level):
		'''make obstacle sprite
		param image: image of obstacle
		param area: area of obstacle, to draw obstacle
		param pos: pos of obstacle
		param level: get attribute of level playing'''
		super().__init__(level=level, group=[level.group_visible, level.group_obstacle])

		self.image = image
		self._rect = pygame.Rect(pos[0], pos[1], area[2], area[3])
		self._hitbox = hitbox
		self.area = area

	def render(self, camera):
		'''
		render image in camera
		param camera: take surface camera to render
		'''
		camera.surface.blit(self.image, camera.apply(self), self.area)
