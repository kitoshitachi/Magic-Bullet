from dataclasses import dataclass
from typing import List
import pygame

@dataclass
class MovingImages:
    up: List[pygame.Surface]
    down: List[pygame.Surface]
    left: List[pygame.Surface]
    right: List[pygame.Surface]
    up_left: List[pygame.Surface]
    up_right: List[pygame.Surface]
    down_left: List[pygame.Surface]
    down_right: List[pygame.Surface]

    def get_images_from_angle(self, angle) -> List[pygame.Surface]:
      if angle <= 22.5:
        return self.right
      elif angle <= 67.5:
        return self.down_right
      elif angle <= 112.5:
        return self.down
      elif angle <= 157.5:
        return self.down_left
      elif angle <= 202.5:
        return self.left
      elif angle <= 247.5:
        return self.up_left
      elif angle <= 292.5:
        return self.up
      elif angle <= 337.5:
        return self.up_right
      else:
        return self.right
         

class Assets():
  grass_tileset: pygame.Surface = None
  water_tileset : pygame.Surface = None
  chip_tileset: pygame.Surface = None
  player: pygame.Surface = None
  frog: MovingImages = None

  def init():
    Assets.grass_tileset = pygame.image.load('graphics/pipoya_grass.png').convert_alpha()
    Assets.water_tileset = pygame.image.load('graphics/pipoya_water.png').convert_alpha()
    Assets.chip_tileset = pygame.image.load('graphics/pipoya_chip.png').convert_alpha()
    Assets.player = pygame.image.load('graphics/test/player.png').convert_alpha()
    Assets.bullet = pygame.image.load('graphics/test/BulletProjectile.png').convert_alpha()
    frog_img = pygame.image.load('graphics/NPC/frog.png').convert_alpha()
    
    Assets.frog = MovingImages(
        *(Assets._create_animation_sprites(frog_img, i, 2, (32, 32)) for i in range(8))
    )

  def _create_animation_sprites(src, row, amount, sprite_size) -> pygame.Surface:
    sprites = []
    for i in range(amount):
      img = pygame.Surface(sprite_size, pygame.SRCALPHA)
      img.blit(src, (0, 0), (i * sprite_size[0], row * sprite_size[1], *sprite_size))
      sprites.append(img)

    return sprites


