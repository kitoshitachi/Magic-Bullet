import pygame

class Bullet:
    def __init__(self, pos, angle):

        self.direction = pygame.math.Vector2(6,0).rotate(angle)
        self.rect = pygame.Rect(center = pos)
    
    def update(self):
        self.rect.x += self.direction.x
        self.rect.y += self.direction.y

        