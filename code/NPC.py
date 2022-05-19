import itertools
from random import randint
import pygame
from assets import Assets
from sprite_animation import SpriteAnimation
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
      image=Assets.frog.up_idle[0],
      hitbox_inflation=(-8, -8),
      pos=pos,
      direction=pygame.math.Vector2(randint(0, 1), randint(0, 1)),
      speed=300)

    self.animation = SpriteAnimation(self, Assets.frog.down_idle, 4)
    self.step = 0
    self.max_step = randint(80,120)
    #movement
    self.memory_direction = pygame.math.Vector2(randint(0,1),randint(0,1))
    self.default = pygame.math.Vector2(1,0)
    self.time_to_live = randint(1,4)
    self.original_image = self.image

    self.angle = pygame.Vector2()
    self.player = None

  def obstacle_collision(self):
    obstacles_and_boundary = itertools.chain(self.level.group_obstacle, self.level.group_boundary)
    CollisionEngine.detect_multiple(self, obstacles_and_boundary, CollisionResponse.slide)

  def see_player(self):
    return False

  def hit(self):
    self.time_to_live -= 1

  def randomMove(self):
    if self.step >= self.max_step:
      self.step = 0
      self.max_step = randint(40,60)

      if randint(0, 3) == 0:
        return

      self.angle = randint(0, 360)
      self.direction = pygame.math.Vector2(1, 0).rotate(self.angle)
      self.animation.set_images(Assets.frog.get_move_sequence_from_angle(self.angle))

  def update(self, delta_time):
    if self.see_player() == True:
      Utils.face_toward(self,self.player.rect.center)
    else:
      self.randomMove()
    
    self.animation.update(delta_time)
      
    self.obstacle_collision()
    self.step += 1
    if self.time_to_live <= 0:
      self.kill()

