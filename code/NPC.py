from random import randint
import pygame
<<<<<<< HEAD
=======
from collision import CollisionEngine, CollisionResponse
>>>>>>> 03df69a03265a2e25cdfdb1e5a8f867c9fae577d
from game_object import GameObject
from utils import Utils
from debug import debug
class NPC(GameObject):
<<<<<<< HEAD
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
=======
  Amount = 0
  def __init__(self, pos, level):
    NPC.Amount += 1
    super().__init__(
      group=[level.visible_sprites, level.NPC_sprites],
      image_path='graphics/test/player.png',
      hitbox_inflation=(0, -26),
      pos=pos,
      direction=pygame.math.Vector2(randint(0, 1), randint(0, 1)),
      speed=300)
>>>>>>> 03df69a03265a2e25cdfdb1e5a8f867c9fae577d

    self.level = level
    self.step = 0
    self.max_step = randint(80,120)
    #movement
    self.memory_direction = pygame.math.Vector2(randint(0,1),randint(0,1))
    self.default = pygame.math.Vector2(1,0)
    self.time_to_live = randint(1,4)
    self.original_image = self.image

    self.player = None

  def obstacle_collision(self):
    CollisionEngine.detect_multiple(self, self.level.obstacle_sprites, CollisionResponse.slide)
    
  def bullet_collision(self):
    for bullet in pygame.sprite.spritecollide(self,self.level.bullet_sprites,True):
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
    

  def update(self, delta_time):
    if self.see_player() == True:
      Utils.face_toward(self,self.player.rect.center)
    else:
      self.randomMove()
      
    self.obstacle_collision()
    self.step += 1
    self.bullet_collision()
    if self.time_to_live <= 0:
      self.kill()

