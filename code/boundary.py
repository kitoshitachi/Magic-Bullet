from math import floor
import pygame
from assets import Assets
from game_object import GameObject
from settings import *


class Boundary(GameObject):
  def __init__(self, pos, hitbox, level):
    super().__init__(level, image=Assets.player, group=[level.group_boundary])

    self.rect = hitbox.copy()
    self.hitbox = hitbox

  def render(self, offset):
    pass
