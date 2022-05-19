from matplotlib import animation, image
class SpriteAnimation():
  def __init__(self, target, images, animation_speed=60, loop=True):
    self.images = images
    self.target = target
    self.animation_speed = animation_speed
    self.loop = loop

    self.current_frame = 0
    self.ended = False

  def update(self, delta_time):
    self.current_frame += self.animation_speed * delta_time

    length = len(self.images)
    if self.current_frame >= length:
      if self.loop:
        self.current_frame -= (self.current_frame // length) * length
      else:
        self.current_frame = length - 1
        self.ended = True

    self.target.image = self.images[int(self.current_frame)]

  def get_current_frame(self):
    return int(self.current_frame)

  def is_animation_ended(self):
    return self.ended 

  def set_images(self, images, reset=True):
    self.images = images
    if reset:
      self.current_frame = 0

  def set_animation_speed(self, speed):
    self.animation_speed = speed
  
