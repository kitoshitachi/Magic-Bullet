import itertools
from random import choice, randint
import pygame
from assets import Assets
from utils import Utils
from settings import *
from sprite_animation import SpriteAnimation
from collision import CollisionEngine, CollisionResponse
from game_object import GameObject

class NPC(GameObject):
	Amount = 0
	def __init__(self, pos, level):
		'''create the NPC of game
		param pos: the start position of NPC
		param level: take the attribute of level
		'''
		NPC.Amount += 1
		super().__init__(
			level=level,
			group=[level.group_visible, level.group_NPC],
			image=Assets.frog.up_idle[0],
			hitbox_inflation=(-8, -8),
			pos=pos,
			direction=pygame.math.Vector2(randint(0, 1), randint(0, 1)),
			speed=300)

		self.Ox = pygame.math.Vector2(1, 0)
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
		'''
		handle collsion obstacle
		'''
		obstacles_and_boundary = itertools.chain(self.level.group_obstacle, self.level.group_boundary)
		CollisionEngine.detect_multiple(self, obstacles_and_boundary, CollisionResponse.slide)

	def has_wall_on_sight(self,line):
		'''check wall on sigh
		param line: the line between player and npc
		return True if has wall on sight else False'''
		for wall in self.level.group_obstacle:
			if len(pygame.Rect.clipline(wall.rect,line)) > 0:
				return True
		return False

	def target(self):
		'''get the player on sight'''
		d_min = SCREEN_WIDTH
		for player in self.level.group_player:
			dist = Utils.distance(self.rect.center,player.rect.center)
			
			if dist > 10*32 or self.has_wall_on_sight((self.rect.center,player.rect.center)):
				continue
			elif d_min > dist:
				self.player = player
				d_min = dist

	def hit(self):
		'''take hit'''
		self.time_to_live -= 1

		if self.time_to_live <= 0:
			return self.mp
		else:
			return 0

	def random_move(self):
		'''random moving npc'''
		if self.step >= self.max_step:
			self.step = 0
			self.max_step = randint(40,60)

			if randint(0, 3) == 0:
				self.direction = pygame.math.Vector2()
				return

			self.angle = randint(0, 360)
			self.direction = self.Ox.rotate(self.angle)
			self.animation.set_images(Assets.frog.move_squence(self.angle))

	def avoid_mobs(self):
		'''avoid mobs around'''
		for NPC in self.level.group_NPC:
			if NPC != self:
				dist = Utils.distance(self.rect.center,NPC.rect.center)
				if 0 < dist < AVOID_RADIUS:
					self.direction += pygame.Vector2(dist).normalize()

	def update(self, delta_time):
		'''update npc at this FPS
		param delta_time: FPS'''
		# self.target()
		if self.player is None: #or self.player.mp < 10:
			self.random_move()
		else:
			pass
			# dx = self.player.rect.centerx - self.rect.centerx
			# dy = self.player.rect.centery - self.rect.centery
			# self.angle = degrees(atan2(dy, dx))
			# self.avoid_mobs()

			# self.direction = self.Ox.rotate(self.angle)
			# self.animation.set_images(Assets.frog.move_squence(self.angle))
			# self.player = None
		
		self.animation.update(delta_time)
			
		self.obstacle_collision()
		self.update_animation(delta_time)

		self.step += 1
		if self.time_to_live <= 0:
			self.kill()
			NPC.Amount -= 1

	def update_animation(self, delta_time):
		'''
		update the animation of NPC at this FPS
		param delta_time: FPS
		'''
		if self.direction.x == 0 and self.direction.y == 0:
			self.animation.set_images(Assets.frog.idle_sequence(self.sprite_angle), reset=False)
		else:
			self.sprite_angle = pygame.Vector2(1, 0).angle_to(self.direction)
			self.animation.set_images(Assets.frog.move_squence(self.sprite_angle), reset=False)

		self.animation.update(delta_time)
	
