import pygame, sys
from assets import Assets
from settings import *
from level import Level

class Game:
	def __init__(self):
		pygame.init()
		
		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE | pygame.SCALED)
		self.display_surface = pygame.display.get_surface()
		Assets.init()

		pygame.display.set_caption('Magic Bullet')
  
		self.level = Level('map1')
		self.clock = pygame.time.Clock()

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

				if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
					pygame.display.toggle_fullscreen()


			delta_time = self.clock.tick(FPS) / 1000.0
			self.screen.fill('black')
			self.level.run(delta_time)

			pygame.display.update()


if __name__ == '__main__':
	game = Game()
	game.run()