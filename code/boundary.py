from game_object import GameObject
from settings import *


class Boundary(GameObject):
	def __init__(self, pos, hitbox, level):
		'''
		make boundary of map
		param pos: pos of boundaray
		param level: get attribute level
		'''
		super().__init__(level, group=[level.group_boundary])

		self._rect = hitbox.copy()
		self._hitbox = hitbox

	def render(self, offset):
		pass
