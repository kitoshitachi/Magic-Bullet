import pygame

class Camera:
    def __init__(self, map_size, screen_size):
        '''make the camera'''
        self.surface = pygame.Surface(screen_size)
        self.camera = pygame.Rect(0, 0, *map_size)
        self.map_size = map_size
        self.width,self.height = screen_size

    def apply(self, entity):
        '''change the pos entity when camera scrooling
        param entity: take the sprite have rect'''
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        '''change the rect when camera scrooling'''
        return rect.move(self.camera.topleft)

    def update(self, target):
        '''
        update the camera
        param target: the target center of camera, ex: player
        '''
        camera_w, camera_h = self.surface.get_size()
        width, height = self.map_size
        x = -target.rect.centerx + int(camera_w / 2)
        y = -target.rect.centery + int(camera_h / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(width - camera_w), x)  # right
        y = max(-(height - camera_h), y)  # bottom
        self.camera = pygame.Rect(x, y, width, height)
