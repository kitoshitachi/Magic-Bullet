import pygame
from utils import Utils
from level import Level

class NPC(pygame.sprite.Sprite):
	def __init__(self, pos,Level:Level):
		self.visible_sprites = Level.visible_sprites
		super().__init__(self.visible_sprites)
		self.image = pygame.image.load('../graphics/monsters/bamboo/move/0.png')
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0,-26)

		#movement
		self.direction = pygame.math.Vector2(1,0)
		self.speed = 7
		
		self.original_image = self.image

	def collision_horizontal(self):
		for sprite in self.obstacle_sprites:
			if sprite.hitbox.colliderect(self.hitbox):
				if self.direction.x > 0:  # moving right
					self.hitbox.right = sprite.hitbox.left
					
				elif self.direction.x < 0:  # moving left
					self.hitbox.left = sprite.hitbox.right
		
	def collision_vertical(self):
		for sprite in self.obstacle_sprites:
			if sprite.hitbox.colliderect(self.hitbox):
				if self.direction.y > 0:  # moving down
					self.hitbox.bottom = sprite.hitbox.top
				elif self.direction.y < 0:  # moving up
					self.hitbox.top = sprite.hitbox.bottom

	def update(self):
		self.player = self.findPlayer()
		if self.player != None:
			Utils.face_toward(self,self.player.rect.center)
		Utils.move(self,self.speed)
