import random
from NPC import NPC
import pygame
from camera import Camera
from settings import CREATE_NPC_DURATION, CYAN, SCREEN_WIDTH, SCREEN_HEIGHT
from map_parser import MapParser
from minimap import Minimap 
from player import Player1, Player2

class Level:
  def __init__(self, map_name):
    # get the display surface 
    self.display_surface = pygame.display.get_surface()

    # sprite group setup
    map_parser = MapParser(map_name)
    self.map_ground_image = map_parser.create_map_ground_image()
    self.group_all = pygame.sprite.Group()
    self.group_visible = pygame.sprite.Group()
    self.group_obstacle = pygame.sprite.Group()
    self.group_boundary = pygame.sprite.Group()
    self.group_bullet = pygame.sprite.Group()
    self.group_player = pygame.sprite.Group()
    self.group_NPC = pygame.sprite.Group()

    self.camera_left = Camera(self.map_ground_image.get_size(), (SCREEN_WIDTH/2, SCREEN_HEIGHT))
    self.camera_right = Camera(self.map_ground_image.get_size(), (SCREEN_WIDTH/2, SCREEN_HEIGHT))
    self.cameras = [self.camera_left, self.camera_right]

    # sprite setup
    self.spawn_points = map_parser.create_spawn_points()
    self.create_player()

    self.create_NPC()
    
    # others
    self.draw_debug = False
    self.createNPC_time = 0
    map_parser.init_objects(self)
    # others
    self.minimap = Minimap((16, 16), self.players, map_parser.create_minimap_image())

    pygame.mixer.music.load("audio/MusMus QUEST - 塔 -.mp3")
    pygame.mixer.music.play(-1)

  def create_player(self):
    self.players = [Player1(random.choice(self.spawn_points), self), Player2(random.choice(self.spawn_points), self)]

  def create_NPC(self):
    NPC(random.choice(self.spawn_points),self)
    self.createNPC_time = pygame.time.get_ticks()

  def cooldown_create_NPC(self):
    current_time = pygame.time.get_ticks()
    if NPC.Amount < 10 and current_time - self.createNPC_time >= CREATE_NPC_DURATION:
      self.create_NPC()

  def run(self, delta_time):
    self.cooldown_create_NPC()

    for camera in self.cameras:
      camera.surface.blit(self.map_ground_image, camera.apply_rect(self.map_ground_image.get_rect()))

    game_objs = sorted(self.group_visible.sprites(), key=lambda sprite: sprite.hitbox.centery)
    for game_obj in game_objs:
      game_obj.before_update(delta_time)
      game_obj.update(delta_time)
      game_obj.after_update()

    self.camera_left.update(self.players[0])
    self.camera_right.update(self.players[1])
      
    for game_obj in game_objs:
      for camera in self.cameras:
        game_obj.render(camera)

    keys_press = pygame.key.get_pressed()
    if keys_press[pygame.K_1]:
      self.draw_debug = not self.draw_debug

    if self.draw_debug:
      for game_obj in sorted(self.group_all.sprites(), key=lambda sprite: sprite.hitbox.centery):
        for camera in self.cameras:
          pygame.draw.rect(camera.surface, CYAN, camera.apply_rect(game_obj.hitbox), 1)

    self.display_surface.blit(self.camera_left.surface, (0, 0))
    self.display_surface.blit(self.camera_right.surface, (SCREEN_WIDTH/2, 0))

    self.minimap.update()
    self.minimap.draw()

# class YSortCameraGroup(pygame.sprite.Group):
#   def __init__(self, level):
#     super().__init__()
#     self.display_surface = pygame.display.get_surface()
#     self.draw_debug = False

#     self.level = level

#     # offset dùng để duy chuyển camera 
#     self.offset = pygame.math.Vector2()
    
#     self.map_width, self.map_height = self.level.map_ground_image.get_size()
#     self.half_width = SCREEN_WIDTH // 2
#     self.half_height = SCREEN_HEIGHT // 2

#   def draw(self, target):
#     self.offset.x = target.rect.centerx - self.half_width
#     self.offset.y = target.rect.centery - self.half_height

#     self.offset.x = max(self.offset.x, 0)
#     self.offset.x = min(self.offset.x, self.map_width - SCREEN_WIDTH) 
#     self.offset.y = max(self.offset.y, 0)
#     self.offset.y = min(self.offset.y, self.map_height - SCREEN_HEIGHT)

    

    


