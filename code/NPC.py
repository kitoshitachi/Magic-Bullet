from random import randint
import pygame
from collision import CollisionEngine, CollisionResponse
from game_object import GameObject
from utils import Utils
from debug import debug
class NPC(GameObject):
  Amount = 0
  def __init__(self, pos, level):
    NPC.Amount += 1
    super().__init__(
      level=level,
      group=[level.group_visible, level.group_NPC],
      image_path='graphics/test/player.png',
      hitbox_inflation=(0, -26),
      pos=pos,
      direction=pygame.math.Vector2(randint(0, 1), randint(0, 1)),
      speed=300)

    self.step = 0
    self.max_step = randint(80,120)
    #movement
    self.memory_direction = pygame.math.Vector2(randint(0,1),randint(0,1))
    self.default = pygame.math.Vector2(1,0)
    self.time_to_live = randint(1,4)
    self.original_image = self.image

    self.player = None

  def obstacle_collision(self):
    CollisionEngine.detect_multiple(self, self.level.group_obstacle, CollisionResponse.slide)

  def see_player(self):
    return False

  def hit(self):
    self.time_to_live -= 1

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
    if self.time_to_live <= 0:
      self.kill()

