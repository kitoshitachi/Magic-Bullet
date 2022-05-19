import pygame
class Assets():
  grass_tileset: pygame.Surface = None
  water_tileset : pygame.Surface = None
  chip_tileset: pygame.Surface = None
  player_image: pygame.Surface = None

  def init():
    Assets.grass_tileset = pygame.image.load('graphics/pipoya_grass.png').convert_alpha()
    Assets.water_tileset = pygame.image.load('graphics/pipoya_water.png').convert_alpha()
    Assets.chip_tileset = pygame.image.load('graphics/pipoya_chip.png').convert_alpha()
    Assets.player_image = pygame.image.load('graphics/test/player.png').convert_alpha()
