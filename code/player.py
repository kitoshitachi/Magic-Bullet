import pygame
from bullet import Bullet
from collision import CollisionEngine, CollisionResponse
from game_object import GameObject
from utils import Utils
from settings import *
from math import atan2,degrees


class Player(GameObject):
  def __init__(self, pos, level):		
    super().__init__(
      group=[level.visible_sprites, level.player_sprites],
      image_path='graphics/test/player.png',
      hitbox_inflation=(-6, -13),
      pos=pos,
      direction=pygame.math.Vector2(0, 0),
      speed=300)

    self.level = level
    self.visible_sprites = level.visible_sprites
    self.obstacle_sprites = level.obstacle_sprites
    self.bullet_sprites = level.bullet_sprites

    #movement
    self.angle = 0
    self.attacking = False
    self.attack_cooldown = 400
    self.attack_time = None
    self.stunt_count_down = 0
    self.prev_stunt_time = 0

    #rotate
    self.original_image = self.image

  def input(self):
    keys_press = pygame.key.get_pressed()
    if keys_press[pygame.K_w]:
      self.direction.y = -1
    elif keys_press[pygame.K_s]:
      self.direction.y = 1
    else:
      self.direction.y = 0

    if keys_press[pygame.K_d]:
      self.direction.x = 1
    elif keys_press[pygame.K_a]:
      self.direction.x = -1
    else:
      self.direction.x = 0

    if self.direction.magnitude() != 0:
      self.direction.normalize_ip()
    
    left_mouse_pressed = pygame.mouse.get_pressed()[0]
    if left_mouse_pressed and not self.attacking:
      self.attacking = True 
      self.attack_time = pygame.time.get_ticks()
      self.shoot()	

  def shoot(self):
    Bullet(self,self.level)

  def obstacle_collision(self):
      CollisionEngine.detect_multiple(self, self.obstacle_sprites, CollisionResponse.slide)
    
  def cooldown(self):
    current_time = pygame.time.get_ticks()

    if self.attacking:
      if current_time - self.attack_time >= self.attack_cooldown:
        self.attacking = False

  def stunted(self):
    self.prev_stunt_time = pygame.time.get_ticks()
    self.stunt_count_down = PLAYER_STUNT_DURATION
    self.direction = pygame.math.Vector2()

  def update(self, delta_time):
    if (self.stunt_count_down <= 0):
      self.input()	
    else:
      self.stunt_count_down -= pygame.time.get_ticks() - self.prev_stunt_time
      self.prev_stunt_time = pygame.time.get_ticks() 
    
    self.cooldown()
    self.obstacle_collision()

    mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())
    mouse_pos += self.level.visible_sprites.offset

    Utils.face_toward(self,mouse_pos)