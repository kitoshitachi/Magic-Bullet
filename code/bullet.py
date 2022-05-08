import itertools
import pygame
from collision import CollisionEngine, CollisionResponse
from game_object import GameObject
from utils import Utils
from settings import BULLET_MAX_TIME_TO_LIVE
from debug import debug

class Bullet(GameObject):
  def __init__(self,player,level):
    self.owner = player
    self.level = level
    
    super().__init__(
      group=[level.visible_sprites, level.bullet_sprites],
      image_path="graphics/test/BulletProjectile.png",
      hitbox_inflation=(-16, -16),
      pos=player.rect.topleft,
      direction=pygame.math.Vector2(1, 0).rotate(player.angle),
      speed=500)

    self.time_to_live = BULLET_MAX_TIME_TO_LIVE

  def obstacle_collision(self):
      def response(collison_data):
          time, _, _, other = collison_data

          if time == 1 or other is self:
            return

          self.time_to_live -= 1
          if self.time_to_live <= 0:
            self.kill()

          CollisionResponse.deflect(collison_data)

      obstacles_and_bullets = itertools.chain(self.level.bullet_sprites, self.level.obstacle_sprites)
      CollisionEngine.detect_multiple(self, obstacles_and_bullets, response)
      self.direction = self.vel.normalize()


  def player_collision(self):
    for player in pygame.sprite.spritecollide(self,self.level.player_sprites,False):
      if player is not self.owner or self.time_to_live != BULLET_MAX_TIME_TO_LIVE:
        self.stunt_count_down = 500
        player.stunted()
        self.kill()

  def update(self, delta_time):
    self.player_collision()
    self.obstacle_collision()


    