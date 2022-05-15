from math import floor
import pygame
from tilesets import Tilesets
from game_object import GameObject
from settings import *


class Boundary(GameObject):
  def __init__(self, pos, hitbox, level):
    super().__init__(level, group=[level.boundary_sprites])

    self.rect = hitbox.copy()
    self.hitbox = hitbox

  def render(self, offset):
    pass
