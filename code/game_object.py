from utils import Utils 
import pygame

class GameObject(pygame.sprite.Sprite):
  def __init__(self, level, group, image_path=None, hitbox_inflation=(0, 0), pos=(0, 0), direction=pygame.math.Vector2(), speed=0):
    group.append(level.group_all)
    super().__init__(group)
    self.level = level
    self.display_surface = pygame.display.get_surface()
    self.direction = direction
    self.speed = speed
    self.vel = direction * 0

    if image_path is None:
      return

    self.image = pygame.image.load(image_path).convert_alpha()
    self.rect = self.image.get_rect(topleft=pos)
    self.hitbox = self.rect.inflate(*hitbox_inflation)

  def render(self, offset):
    self.display_surface.blit(self.image, self.rect.topleft - offset)

  def before_update(self, delta_time):
    self.vel = self.direction * (self.speed * delta_time)

  def update(self, delta_time):
      pass

  def after_update(self):
    vel_x, vel_y = Utils.round_away_from_zero(self.vel.x), Utils.round_away_from_zero(self.vel.y)
    self.hitbox.x += vel_x
    self.hitbox.y += vel_y

    self.rect.x += vel_x
    self.rect.y += vel_y
    
    
