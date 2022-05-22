from math import sqrt,floor,ceil

class Utils:
	'''class utils'''
	@staticmethod
	def distance(pos_1, pos_2):
		'''caculator distance of two points'''
		dx = pos_1[0] - pos_2[0]
		dy = pos_1[1] - pos_2[1]
		return sqrt(dx**2 + dy**2)

	@staticmethod
	def round_away_from_zero(x):
		'''round x, mixing value if value = 0.5'''
		return int(floor(x + 0.5) if x > 0 else ceil(x - 0.5))

