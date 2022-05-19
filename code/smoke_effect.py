from matplotlib import animation
import pygame
from sprite_animation import SpriteAnimation
from game_object import GameObject


class SmokeEffect(GameObject):
  FIRE_SFX = pygame.mixer.Sound("audio/reflect.wav")
  FIRE_SFX.set_volume(0.4)

  def __init__(self, pos, level):
      super().__init__(level, [level.group_visible], pos=pos)
      self.animation = SpriteAnimation(self, [
        pygame.image.load(f"./graphics/smoke_effect/{i}.png").convert_alpha() for i in range(7)
      ], loop=False)

      SmokeEffect.FIRE_SFX.play();

  def update(self, delta_time):
      super().update(delta_time)
      self.animation.update(delta_time)

      if (self.animation.is_animation_ended()):
        self.kill()
