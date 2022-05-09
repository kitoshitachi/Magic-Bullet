from math import floor
import pygame
from tilesets import Tilesets
from game_object import GameObject
from settings import *


class Obstacle(GameObject):
  def __init__(self, image, area, pos, hitbox, level):
<<<<<<< HEAD
    super().__init__([level.visible_sprites, level.obstacle_sprites])
=======
    super().__init__(group=[level.visible_sprites, level.obstacle_sprites])
>>>>>>> 03df69a03265a2e25cdfdb1e5a8f867c9fae577d

    self.image = image
    self.rect = pygame.Rect(pos[0], pos[1], area[2], area[3])
    self.hitbox = hitbox
    self.area = area

  def render(self, offset):
    self.display_surface.blit(self.image, self.rect.topleft - offset, self.area)
