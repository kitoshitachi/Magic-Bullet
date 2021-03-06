import pygame
from game_object import GameObject 
from settings import *


class Wall(GameObject):
	def __init__(self,pos,level):
		'''
		create walls
		param pos: position of wall
		param level: to take group of wall
		'''
		super().__init__([level.group_obstacle])

		self._rect = pygame.Rect(pos[0], pos[1], TILESIZE, TILESIZE)
		self._hitbox = self._rect.inflate(0, -5)
