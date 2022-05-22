import itertools
import pygame
from assets import Assets
from settings import *
from smoke_effect import SmokeEffect
from collision import CollisionEngine, CollisionResponse
from game_object import GameObject
from utils import Utils
from settings import BULLET_MAX_TIME_TO_LIVE

class Bullet(GameObject):
	FIRE_SFX = pygame.mixer.Sound(AUDIO_PATH + 'bullet_fire.wav')
	FIRE_SFX.set_volume(0.3)

	def __init__(self,player,level):
		'''the bullet class
		param player: the sprite make bullet
		param level: get the attribute level
		'''
		self.owner = player
		super().__init__(
		level=level,
		group=[level.group_visible, level.group_bullet],
		image=Assets.bullet_img,
		hitbox_inflation=(-16, -16),
		pos=player.hitbox.topleft,
		_direction=pygame.math.Vector2(1, 0).rotate(player.angle),
		speed=500)

		self.time_to_live = BULLET_MAX_TIME_TO_LIVE
		
		# đạn nằm ở giữa hitbox người bắn
		self._rect.center = player.hitbox.center
		self._hitbox.center = player.hitbox.center

		Bullet.FIRE_SFX.play()

	def obstacle_collision(self):
		'''handle obstacle collision'''
		def response(collison_data):
			time, normal, _, obstacle = collison_data

			if obstacle is self:
				return

			self.time_to_live -= 1
			if self.time_to_live <= 0:
				self.kill()
			
			smoke_pos = (self._hitbox.centerx + Utils.round_away_from_zero(self._vel.x * time) - (TILESIZE / 2), 
						self._hitbox.centery + Utils.round_away_from_zero(self._vel.y * time) - (TILESIZE / 2))

			SmokeEffect(smoke_pos, self._level)

			CollisionResponse.deflect(collison_data)
			
			# đảo chiểu của viên đạn còn lại
			if (isinstance(obstacle, Bullet)):
				other_bullet: Bullet = obstacle
				other_bullet._direction.reflect_ip(normal * -1)
				other_bullet.time_to_live -= 1

				for bullet in [self, other_bullet]:
					if bullet.hitbox.colliderect(self.owner.hitbox):
						self.owner.stunted()
						bullet.kill()

		obstacles_and_bullets = itertools.chain(self._level.group_bullet, self._level.group_obstacle)
		CollisionEngine.detect_multiple(self, obstacles_and_bullets, response)
		self._direction = self._vel.normalize()

	def player_collision(self):
		'''handle player collision'''
		def response(collison_data):
			time, _, _, player = collison_data

			if player is self.owner:
				player.stunted()
			else:
				player.kill()

			smoke_pos = (self._hitbox.centerx + Utils.round_away_from_zero(self._vel.x * time) - (TILESIZE / 2),
						self._hitbox.centery + Utils.round_away_from_zero(self._vel.y * time) - (TILESIZE / 2))
			SmokeEffect(smoke_pos, self._level)

			self.kill()

		CollisionEngine.detect_multiple(self, self._level.group_player, response)

	def npc_collision(self):
		'''handle npc collision'''
		def response(collison_data):
			time, _, _, npc = collison_data
			smoke_pos = (self._hitbox.centerx + Utils.round_away_from_zero(self._vel.x * time) - (TILESIZE / 2),
							self._hitbox.centery + Utils.round_away_from_zero(self._vel.y * time) - (TILESIZE / 2))
			SmokeEffect(smoke_pos, self._level)

			self.owner.mp += npc.hit()
			self.kill()

		CollisionEngine.detect_multiple(self, self._level.group_NPC, response)

	def update(self, delta_time):
		'''update bullet after FPS
		param delta_time: FPS'''
		self.player_collision()
		self.obstacle_collision()
		self.npc_collision()