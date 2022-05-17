from matplotlib import animation
from numpy import True_

from settings import FPS


class SpriteAnimation():
  def __init__(self, target, images, animation_speed=1, loop=True):
    self.images = images
    self.target = target
    self.animation_speed = animation_speed
    self.loop = loop

    self.current_frame = 0
    self.ended = False

  def update(self, delta_time):
    self.current_frame += self.animation_speed * delta_time * FPS

    length = len(self.images)
    if self.current_frame >= length:
      if self.loop:
        self.current_frame -= (self.current_frame // length) * self.current_frame;
      else:
        self.current_frame = length - 1
        self.ended = True_

    self.target.image = self.images[int(self.current_frame)]
    self.target.rect = self.target.image.get_rect(center = self.target.hitbox.center)

  def get_current_frame(self):
    return int(self.current_frame)

  def is_animation_ended(self):
    return self.ended 


  
