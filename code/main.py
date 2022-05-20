import pygame, sys
from assets import Assets
from pause_menu import PauseMenu
from main_menu import MainMenu
from settings import *
from level import Level

class Game:
	
	def __init__(self):
		pygame.init()
		
		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE | pygame.SCALED)
		self.display_surface = pygame.display.get_surface()
		Assets()

		self.main_menu = MainMenu(self.start_game, self.display_surface)
		self.pause_menu = PauseMenu(self.resume_game, self.to_main_menu, self.display_surface)
		
		pygame.display.set_caption('Magic Bullet')
  
		self.level = Level('map1', self.to_main_menu)
		self.clock = pygame.time.Clock()

		self.paused = False
		self.handle = self.run_menu

	def start_game(self):
		self.handle = self.run_level

	def resume_game(self):
		self.paused = False

	def to_main_menu(self):
		self.handle = self.run_menu
		self.level = Level('map1', self.to_main_menu)
		self.paused = False
		self.pause_menu.reset()

	def run(self): 
		while True:
			events = pygame.event.get()
			for event in events:
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

				if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
					pygame.display.toggle_fullscreen()

			delta_time = self.clock.tick(FPS) / 1000.0

			self.handle(events, delta_time)

			pygame.display.update()

	def run_menu(self, events, _):
		self.main_menu.run(events)

	def run_level(self, events, delta_time):
		for event in events:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and self.paused == False:
				self.paused = True
				self.pause_menu.take_screen_shot()

		if self.paused:
			self.pause_menu.run(events)
		else:
			self.screen.fill('black')
			self.level.run(events, delta_time)

if __name__ == '__main__':
	game = Game()
	game.run()