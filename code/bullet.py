import itertools
import pygame
from settings import TILESIZE
from smoke_effect import SmokeEffect
from collision import CollisionEngine, CollisionResponse
from game_object import GameObject
from utils import Utils
from settings import BULLET_MAX_TIME_TO_LIVE
from debug import debug

class Bullet(GameObject):
  FIRE_SFX = pygame.mixer.Sound("audio/bullet_fire.wav")
  FIRE_SFX.set_volume(0.3)

  def __init__(self,player,level):
    self.owner = player
    super().__init__(
      level=level,
      group=[level.group_visible, level.group_bullet],
      image_path="graphics/test/BulletProjectile.png",
      hitbox_inflation=(-16, -16),
      pos=player.hitbox.topleft,
      direction=pygame.math.Vector2(1, 0).rotate(player.angle),
      speed=500)

    self.time_to_live = BULLET_MAX_TIME_TO_LIVE
    
    # đạn nằm ở giữa hitbox người bắn
    self.rect.center = player.hitbox.center
    self.hitbox.center = player.hitbox.center

    Bullet.FIRE_SFX.play()

  def obstacle_collision(self):
      def response(collison_data):
          time, normal, _, obstacle = collison_data

          if obstacle is self:
            return

          self.time_to_live -= 1
          if self.time_to_live <= 0:
            self.kill()
          
          smoke_pos = (self.hitbox.centerx + Utils.round_away_from_zero(self.vel.x * time) - (TILESIZE / 2), 
                       self.hitbox.centery + Utils.round_away_from_zero(self.vel.y * time) - (TILESIZE / 2))
          

          SmokeEffect(smoke_pos, self.level)

          CollisionResponse.deflect(collison_data)
          
          # đảo chiểu của viên đạn còn lại
          if (isinstance(obstacle, Bullet)):
            obstacle.direction.reflect_ip(normal * -1)

      obstacles_and_bullets = itertools.chain(self.level.group_bullet, self.level.group_obstacle)
      CollisionEngine.detect_multiple(self, obstacles_and_bullets, response)
      self.direction = self.vel.normalize()

  def player_collision(self):
    def response(collison_data):
      time, _, _, player = collison_data

      if player is self.owner and self.time_to_live != BULLET_MAX_TIME_TO_LIVE:
        self.stunt_count_down = 500
        player.stunted()
      else:
        player.kill()

      smoke_pos = (self.hitbox.centerx + Utils.round_away_from_zero(self.vel.x * time) - (TILESIZE / 2),
                   self.hitbox.centery + Utils.round_away_from_zero(self.vel.y * time) - (TILESIZE / 2))
      SmokeEffect(smoke_pos, self.level)

      self.kill()

    CollisionEngine.detect_multiple(self, self.level.group_player, response)

  def npc_collision(self):
    def response(collison_data):
      time, _, _, npc = collison_data
      smoke_pos = (self.hitbox.centerx + Utils.round_away_from_zero(self.vel.x * time) - (TILESIZE / 2),
                    self.hitbox.centery + Utils.round_away_from_zero(self.vel.y * time) - (TILESIZE / 2))
      SmokeEffect(smoke_pos, self.level)

      npc.hit()

    CollisionEngine.detect_multiple(self, self.level.group_NPC, response)

  def update(self, delta_time):
    self.player_collision()
    self.obstacle_collision()
    self.npc_collision()


    