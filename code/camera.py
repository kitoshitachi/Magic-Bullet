import pygame

class Camera:
    def __init__(self, map_size, screen_size):
        self.surface = pygame.Surface(screen_size)
        self.camera = pygame.Rect(0, 0, *map_size)
        self.map_size = map_size

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        camera_w, camera_h = self.surface.get_size()
        map_w, map_h = self.map_size
        x = -target.rect.centerx + int(camera_w / 2)
        y = -target.rect.centery + int(camera_h / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(map_w - camera_w), x)  # right
        y = max(-(map_h - camera_h), y)  # bottom
        self.camera = pygame.Rect(x, y, map_w, map_h)
