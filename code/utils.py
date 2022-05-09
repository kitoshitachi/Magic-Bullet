from math import atan2, degrees
import math
import pygame

class Utils:

	@staticmethod
	def face_toward(object, pos):
		original_rect = object.rect
		dx, dy = pos.x - original_rect.centerx , pos.y - original_rect.centery
		object.angle = degrees(atan2(dy, dx))
		object.image = pygame.transform.rotate(object.original_image, -object.angle)
		object.rect = object.image.get_rect(center=original_rect.center)

	@staticmethod
	def move(object,speed):
		if object.direction.magnitude() != 0:
			object.direction.normalize_ip()

		object.hitbox.x += object.direction.x * speed
		object.collision_horizontal()
		
		object.hitbox.y += object.direction.y * speed
		object.collision_vertical()

		object.rect.center = object.hitbox.center

		import math

	@staticmethod
	def round_away_from_zero(x):
		return int(math.floor(x + 0.5) if x > 0 else math.ceil(x - 0.5))
