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
      pos=player.hitbox.topleft,
      direction=pygame.math.Vector2(1, 0).rotate(player.angle),
      speed=500)

    self.time_to_live = BULLET_MAX_TIME_TO_LIVE
    
    # đạn nằm ở giữa hitbox người bắn
    self.rect.center = player.hitbox.center
    self.hitbox.center = player.hitbox.center

  def obstacle_collision(self):
      def response(collison_data):
          _, normal, _, obstacle = collison_data

          if obstacle is self:
            return

          self.time_to_live -= 1
          if self.time_to_live <= 0:
            self.kill()

          CollisionResponse.deflect(collison_data)
          
          # đảo chiểu của viên đạn còn lại
          if (isinstance(obstacle, Bullet)):
            obstacle.direction.reflect_ip(normal * -1)

      obstacles_and_bullets = itertools.chain(self.level.bullet_sprites, self.level.obstacle_sprites)
      CollisionEngine.detect_multiple(self, obstacles_and_bullets, response)
      self.direction = self.vel.normalize()


  def player_collision(self):
    def response(collison_data):
      player = collison_data[3]
      if player is not self.owner or self.time_to_live != BULLET_MAX_TIME_TO_LIVE:
        self.stunt_count_down = 500
        player.stunted()
        self.kill()

    CollisionEngine.detect_multiple(self, self.level.player_sprites, response)



  def update(self, delta_time):
    self.player_collision()
    self.obstacle_collision()


    