import random
from typing import List
from NPC import NPC
import pygame
from camera import Camera
from settings import *
from map_parser import MapParser
from player import Player, Player1, Player2

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
		self.players = self.create_player()

		self.create_NPC()
		
		# others
		self.draw_debug = False
		self.createNPC_time = 0
		map_parser.init_objects(self)
		# others
		# self.minimap = Minimap((16, 16), self.players, map_parser.create_minimap_image())

		pygame.mixer.music.load("audio/MusMus QUEST - 塔 -.mp3")
		pygame.mixer.music.play(-1)

	def create_player(self) -> List[Player]:
		return [Player1(random.choice(self.spawn_points), self), Player2(random.choice(self.spawn_points), self)]

	def create_NPC(self):
		NPC(random.choice(self.spawn_points),self)
		self.createNPC_time = pygame.time.get_ticks()

	def cooldown_create_NPC(self):
		current_time = pygame.time.get_ticks()
		if NPC.Amount < 10 and current_time - self.createNPC_time >= CREATE_NPC_DURATION:
			self.create_NPC()

	def run(self, delta_time):
		self.cooldown_create_NPC()

		game_objs = sorted(self.group_visible.sprites(), key=lambda sprite: sprite.hitbox.centery)
		for game_obj in game_objs:
			game_obj.before_update(delta_time)
			game_obj.update(delta_time)
			game_obj.after_update()

		self.camera_left.update(self.players[0])
		self.camera_right.update(self.players[1])
			
		for camera in self.cameras:
			camera.surface.blit(self.map_ground_image, camera.apply_rect(self.map_ground_image.get_rect()))

		for game_obj in game_objs:
			for camera in self.cameras:
				game_obj.render(camera)

		keys_press = pygame.key.get_pressed()
		if keys_press[pygame.K_1]:
			self.draw_debug = not self.draw_debug

		if self.draw_debug:
			for game_obj in self.group_all.sprites():
				for camera in self.cameras:
					pygame.draw.rect(camera.surface, CYAN, camera.apply_rect(game_obj.hitbox), 1)

		player_bar = PLAYER_MANA_BAR.copy()
		player_bar.x = (self.camera_left.width - player_bar.width)/2
		player_bar.y = self.camera_left.height - 40
		self.draw_bar(self.camera_left.surface, player_bar.copy(), self.players[0].mp / PLAYER_MANA)
		self.draw_bar(self.camera_right.surface, player_bar.copy(), self.players[1].mp / PLAYER_MANA)
		player_bar.y +=20
		self.draw_bar(self.camera_left.surface, player_bar.copy(), self.players[0].stamina / PLAYER_STAMINA,ORANGE)
		self.draw_bar(self.camera_right.surface, player_bar.copy(), self.players[1].stamina / PLAYER_STAMINA,ORANGE)
		player_bar.y -= 25
		player_bar.height = 5
		pct = self.players[0].attack_timer.elapsed_time/ATTACK_COOLDOWN
		if pct:
			self.draw_bar(self.camera_left.surface, player_bar.copy(), pct, DARKGREY)

		pct = self.players[1].attack_timer.elapsed_time/ATTACK_COOLDOWN
		if pct:
			self.draw_bar(self.camera_right.surface, player_bar.copy(), pct, DARKGREY)

		for i in range(2):
			player_bar = self.cameras[i].apply_rect(self.players[i].rect)
			player_bar.height = 7
			pct = self.players[i].stunt_timer.elapsed_time/STUNT_DURATION
			if pct:
				self.draw_bar(self.cameras[i].surface,player_bar.copy(), pct, GREEN)
			
		self.display_surface.blit(self.camera_left.surface, (0, 0))
		self.display_surface.blit(self.camera_right.surface, (SCREEN_WIDTH/2, 0))

		# self.minimap.update()
		# self.minimap.draw()

	@staticmethod
	def draw_bar(surf, bar:pygame.Rect , pct, color = CYAN):
		if pct < 0:
			pct = 0
		fill_rect = bar.copy()
		fill_rect.width = pct * bar.width
		if pct <= 0.3:
			color = RED
		elif pct <= 0.6:
			color = YELLOW

		pygame.draw.rect(surf, color, fill_rect)
		pygame.draw.rect(surf, WHITE, bar, 1)