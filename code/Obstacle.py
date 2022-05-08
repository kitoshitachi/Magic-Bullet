from math import floor
import pygame
from tilesets import Tilesets
from game_object import GameObject
from settings import *


class Obstacle(GameObject):
  def __init__(self, image, area, pos, hitbox, level):
    super().__init__(group=[level.visible_sprites, level.obstacle_sprites])

    self.image = image
    self.rect = pygame.Rect(pos[0], pos[1], area[2], area[3])
    self.hitbox = hitbox
    self.area = area

  def render(self, offset):
    self.display_surface.blit(self.image, self.rect.topleft - offset, self.area)
