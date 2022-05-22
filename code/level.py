import random
import pygame
from NPC import NPC
from camera import Camera
from clock import Countdown
from game_over import GameOver
from settings import *
from map import Map
from player import Player1, Player2
import itertools

class Level:
	def __init__(self, map_name, on_main_menu):
		'''create level game
		param map_name: the map player choose
		param on_main_menu: the event take main menu'''
		# get the display surface 
		self.display_surface = pygame.display.get_surface()

		# sprite group setup
		self.__map = Map(map_name)
		self.__group_all = pygame.sprite.Group()
		self.__group_visible = pygame.sprite.Group()
		self.__group_obstacle = pygame.sprite.Group()
		self.__group_boundary = pygame.sprite.Group()
		self.__group_bullet = pygame.sprite.Group()
		self.__group_player = pygame.sprite.Group()
		self.__group_NPC = pygame.sprite.Group()
		self.camera_left = Camera(self.__map.size, (SCREEN_WIDTH/2, SCREEN_HEIGHT))
		self.camera_right = Camera(self.__map.size, (SCREEN_WIDTH/2, SCREEN_HEIGHT))
		self.cameras = [self.camera_left, self.camera_right]

		# sprite setup
		self.players = self.create_player()

		self.create_NPC()
		
		# others
		self.draw_debug = False
		self.create_NPC_clock = Countdown(CREATE_NPC_DURATION)
		self.__map.init_objects(self)

		self.on_main_menu = on_main_menu
		# others
		self.game_over_timer = Countdown(cooldown=1)
		self.game_over_menu = None

		# self.minimap = Minimap((16, 16), self.players, map_parser.create_minimap_image())
		self.taken = False
		
		pygame.mixer.music.load(AUDIO_PATH + "MusMus QUEST - 塔 -.mp3")
		pygame.mixer.music.play(-1)

	@property
	def group_all(self):
		return self.__group_all

	@property
	def group_visible(self):
		return self.__group_visible

	@property
	def group_obstacle(self):
		return self.__group_obstacle

	@property
	def group_boundary(self):
		return self.__group_boundary

	@property
	def group_bullet(self):
		return self.__group_bullet

	@property
	def group_player(self):
		return self.__group_player
	@property
	def group_NPC(self):
		return self.__group_obstacle

	@property
	def obstacles_and_boundary(self):
		'''get obstacle and boundary group'''
		return itertools.chain(self.__group_obstacle, self.__group_boundary)

	def create_player(self):
		'''create random sample position spawn of players'''
		position = random.sample(self.__map.spawn_points,2)
		return (Player1(position[0], self), Player2(position[1], self))

	def create_NPC(self):
		'''create the npc, use random choice'''
		NPC(random.choice(self.__map.spawn_points),self)
		self.createNPC_time = pygame.time.get_ticks()

	def cooldown_create_NPC(self):
		'''check cooldown create NPC'''
		if NPC.Amount > 10 or self.create_NPC_clock.is_done:
			pass
		else:
			self.create_NPC()

	def run(self, events, delta_time):
		'''run the level , handle event
		param events: the event from game
		param delta_time: FPS 
		'''
		if not (self.game_over_menu is None) and self.game_over_timer.is_done:
			if self.game_over_menu.has_taken_screen_shot():
				self.game_over_menu.run(events)
				return;

		self.cooldown_create_NPC()

		game_objs = sorted(self.__group_visible.sprites(), key=lambda sprite: sprite.hitbox.centery)
		for game_obj in game_objs:
			game_obj.before_update(delta_time)
			game_obj.update(delta_time)
			game_obj.after_update()


		self.camera_left.update(self.players[0])
		self.camera_right.update(self.players[1])
			
		for camera in self.cameras:
			camera.surface.blit(self.__map.ground_layer, camera.apply_rect(self.__map.ground_layer.get_rect()))

		for game_obj in game_objs:
			for camera in self.cameras:
				game_obj.render(camera)

		# debug game
		# keys_press = pygame.key.get_pressed()
		# if keys_press[pygame.K_2]:
		# 	for player in self.players:
		# 		player.mp = PLAYER_MANA

		# if keys_press[pygame.K_1]:
		# 	self.draw_debug = not self.draw_debug

		# if self.draw_debug:
		# 	for game_obj in self.__group_all.sprites():
		# 		for camera in self.cameras:
		# 			pygame.draw.rect(camera.surface, CYAN, camera.apply_rect(game_obj.hitbox), 1)

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

		if self.game_over_menu is None and len(self.__group_player) <= 1:
			if len(self.__group_player) == 0 or isinstance(self.__group_player.sprites()[0], Player1):
				self.game_over_menu = GameOver(self.on_main_menu, self.display_surface, 1)
			else:
				self.game_over_menu = GameOver(self.on_main_menu, self.display_surface, 2)

			self.game_over_timer.reset()

		if not (self.game_over_menu is None) and self.game_over_timer.is_done:
			if not self.game_over_menu.has_taken_screen_shot():
				self.game_over_menu.take_screen_shot()

	@staticmethod
	def draw_bar(surf, bar:pygame.Rect , pct, color = CYAN):
		'''draw the bar
		param surf: surface to draw bar
		param pct: percentage of bar
		param color: default is CYAN'''
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