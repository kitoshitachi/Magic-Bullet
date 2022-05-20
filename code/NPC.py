import itertools
from random import choice, randint
import pygame
from assets import Assets
from settings import *
from sprite_animation import SpriteAnimation
from collision import CollisionEngine, CollisionResponse
from game_object import GameObject
from debug import debug

class NPC(GameObject):
	Amount = 0
	def __init__(self, pos, level):
		NPC.Amount += 1
		super().__init__(
			level=level,
			group=[level.group_visible, level.group_NPC],
			image=Assets.frog.up_idle[0],
			hitbox_inflation=(-8, -8),
			pos=pos,
			direction=pygame.math.Vector2(randint(0, 1), randint(0, 1)),
			speed=300)


		self.animation = SpriteAnimation(self, Assets.frog.down_idle, 4)
		self.step = 0
		self.max_step = randint(80,120)
		#movement
		self.memory_direction = None
		self.default = pygame.math.Vector2(1,0)
		self.time_to_live = choice(RATE)
		self.mp = (self.time_to_live + choice(RATE)) * NPC_MANA
		self.sprite_angle = 0
		self.angle = 0
		self.player = None
	def obstacle_collision(self):
		obstacles_and_boundary = itertools.chain(self.level.group_obstacle, self.level.group_boundary)
		CollisionEngine.detect_multiple(self, obstacles_and_boundary, CollisionResponse.slide)

	def target(self):
		d_max = -1
		for player in self.level.group_player:
			dx = player.rect.x - self.rect.x
			dy = player.rect.y - self.rect.y
			d = dx*dx+dy*dy
			if d <= 32*32*10:
				for wall in self.level.group_obstacle:
					if pygame.Rect.clipline(wall.rect,self.rect.center,player.rect.center) is not None:
						if d > d_max:
							self.player = player
							d_max = d
						break

	def hit(self):
		self.time_to_live -= 1
		if self.time_to_live <= 0:
			return self.mp
		else:
			return 0

	def random_move(self):
		if self.step >= self.max_step:
			self.step = 0
			self.max_step = randint(40,60)

			if randint(0, 3) == 0:
				self.direction = pygame.math.Vector2()
				return

			self.angle = randint(0, 360)
			self.direction = pygame.math.Vector2(1, 0).rotate(self.angle)
			self.animation.set_images(Assets.frog.get_move_sequence_from_angle(self.angle))

	def update(self, delta_time):
		# self.target()
		if self.player is not None:
			pass
			# self.rect.topleft
			# self.angle = self.direction.angle_to(pygame.math.Vector2(1, 0))
			# self.animation.set_images(Assets.frog.get_move_sequence_from_angle(self.angle))

			# self.player = None
		else:
			self.random_move()
		
		self.animation.update(delta_time)
			
		self.obstacle_collision()
		self.update_animation(delta_time)

		self.step += 1
		if self.time_to_live <= 0:
			self.kill()

	def update_animation(self, delta_time):
		if self.direction.x == 0 and self.direction.y == 0:
			self.animation.set_images(Assets.frog.get_idle_sequence_from_angle(self.sprite_angle), reset=False)
		else:
			self.sprite_angle = pygame.Vector2(1, 0).angle_to(self.direction)
			self.animation.set_images(Assets.frog.get_move_sequence_from_angle(self.sprite_angle), reset=False)

		self.animation.update(delta_time)
	
