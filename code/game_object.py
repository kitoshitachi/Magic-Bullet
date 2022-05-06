import pygame

class GameObject(pygame.sprite.Sprite):
  def __init__(self, group, image_path = None, pos = (0, 0), hitbox_inflation = (0, 0)):
    super().__init__(group)
    self.display_surface = pygame.display.get_surface()
    
    if image_path is None:
      return

    self.image = pygame.image.load(image_path).convert_alpha()
    self.rect = self.image.get_rect(topleft=pos)
    self.hitbox = self.rect.inflate(*hitbox_inflation)

  def render(self, offset):
    self.display_surface.blit(self.image, self.rect.topleft - offset)