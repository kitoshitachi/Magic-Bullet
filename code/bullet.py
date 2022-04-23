import pygame

class Bullet:
    def __init__(self, pos, direction):
        self.speed = 6

        self.direction = direction
        self.rect = pygame.Rect(center = pos)
    
    def update(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        