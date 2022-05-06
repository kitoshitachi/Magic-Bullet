import pygame
from game_object import GameObject 
from settings import *


class Wall(GameObject):
	def __init__(self,pos,level):
		super().__init__([level.obstacle_sprites])

		self.rect = pygame.Rect(pos[0], pos[1], TILESIZE, TILESIZE)
		self.hitbox = self.rect.inflate(0, -5)
