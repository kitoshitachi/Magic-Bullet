from random import randint
import pygame
from game_object import GameObject
from utils import Utils
from debug import debug
class NPC(GameObject):
	Amount = 0
	def __init__(self, pos,Level):
		NPC.Amount += 1
		self.level = Level
		super().__init__([self.level.visible_sprites, self.level.NPC_sprites], 'graphics/test/player.png', pos, (0, -26))
		self.step = 0
		self.max_step = randint(80,120)
		#movement
		self.direction = pygame.math.Vector2(randint(0,1),randint(0,1))
		self.memory_direction = pygame.math.Vector2(randint(0,1),randint(0,1))
		self.default = pygame.math.Vector2(1,0)
		self.speed = 6
		self.time_to_live = randint(1,4)
		self.original_image = self.image

		self.player = None

	def collision_horizontal(self):
		for sprite in self.level.obstacle_sprites:
			if sprite.hitbox.colliderect(self.hitbox):
				if self.direction.x > 0:  # moving right
					self.hitbox.right = sprite.hitbox.left
					
				elif self.direction.x < 0:  # moving left
					self.hitbox.left = sprite.hitbox.right
		
	def collision_vertical(self):
		for sprite in self.level.obstacle_sprites:
			if sprite.hitbox.colliderect(self.hitbox):
				if self.direction.y > 0:  # moving down
					self.hitbox.bottom = sprite.hitbox.top
				elif self.direction.y < 0:  # moving up
					self.hitbox.top = sprite.hitbox.bottom

	def bullet_collision(self):
		for NPC in pygame.sprite.spritecollide(self,self.level.bullet_sprites,True):
			self.time_to_live -=1

	def see_player(self):
		return False

	def randomMove(self):
		if self.step >= self.max_step:
			self.step = 0
			self.max_step = randint(40,60)
			self.direction.x = randint(-1,1)
			self.direction.y = randint(-1,1)
		
		angle = self.direction.angle_to(self.default)
		self.image = pygame.transform.rotate(self.original_image,angle)
		

	def update(self):
		if self.see_player() == True:
			Utils.face_toward(self,self.player.rect.center)
		else:
			self.randomMove()
			
		Utils.move(self,self.speed)
		self.step += 1
		self.bullet_collision()
		if self.time_to_live <= 0:
			self.kill()

