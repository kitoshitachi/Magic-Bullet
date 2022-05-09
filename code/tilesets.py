<<<<<<< HEAD



import pygame


=======
import pygame
>>>>>>> 03df69a03265a2e25cdfdb1e5a8f867c9fae577d
class Tilesets():
  grass_tileset: pygame.Surface = None
  water_tileset : pygame.Surface = None
  chip_tileset : pygame.Surface = None

  def init():
    Tilesets.grass_tileset = pygame.image.load('graphics/pipoya_grass.png').convert_alpha()
    Tilesets.water_tileset = pygame.image.load('graphics/pipoya_water.png').convert_alpha()
    Tilesets.chip_tileset = pygame.image.load('graphics/pipoya_chip.png').convert_alpha()