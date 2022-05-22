import pygame, sys
from assets import Assets
from pause_menu import PauseMenu
from main_menu import MainMenu
from settings import *
from level import Level

class Game:
	
	def __init__(self):
		'''game magic bullet'''
		pygame.init()
		
		self._screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE | pygame.SCALED)
		self.display_surface = pygame.display.get_surface()
		Assets()

		self.main_menu = MainMenu(self._start_game, self.display_surface)
		self.pause_menu = PauseMenu(self._resume_game, self._to_main_menu, self.display_surface)
		
		pygame.display.set_caption('Magic Bullet')
  
		self._level = Level('map1', self._to_main_menu)
		self.clock = pygame.time.Clock()

		self._paused = False
		self._handle = self._run_menu

	def _start_game(self):
		'''set event start game'''
		self._handle = self._run_level

	def _resume_game(self):
		'''set event resume game'''
		self._paused = False

	def _to_main_menu(self):
		''''''
		self._handle = self._run_menu
		self._level = Level('map1', self._to_main_menu)
		self._paused = False
		self.pause_menu.reset()

	def run(self):
		'''run game'''
		while True:
			events = pygame.event.get()
			for event in events:
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

				if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
					pygame.display.toggle_fullscreen()

			delta_time = self.clock.tick(FPS) / 1000.0

			self._handle(events, delta_time)

			pygame.display.update()

	def _run_menu(self, events,_):
		'''run main menu'''
		self.main_menu.run(events)

	def _run_level(self, events, delta_time):
		'''
		run _level with FPS
		param events: _handle event
		param delta: FPS
		'''
		for event in events:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and self._paused == False:
				self._paused = True
				self.pause_menu.take_screen_shot()

		if self._paused:
			self.pause_menu.run(events)
		else:
			self._screen.fill('black')
			self._level.run(events, delta_time)

if __name__ == '__main__':
	game = Game()
	game.run()