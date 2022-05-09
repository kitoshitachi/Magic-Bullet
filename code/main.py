import pygame, sys
from tilesets import Tilesets
from settings import *
from level import Level

class Game:
	def __init__(self):
		pygame.init()
		
<<<<<<< HEAD
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE | pygame.SCALED)
=======
		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE | pygame.SCALED)
>>>>>>> 03df69a03265a2e25cdfdb1e5a8f867c9fae577d
		self.display_surface = pygame.display.get_surface()
		Tilesets.init()

		pygame.image.load('graphics/pipoya_grass.png').convert_alpha()
  
		pygame.display.set_caption('Magic Bullet')
  
		self.level = Level('map1')
		self.clock = pygame.time.Clock()

<<<<<<< HEAD
		self.level = Level('map1')
	
=======
>>>>>>> 03df69a03265a2e25cdfdb1e5a8f867c9fae577d
	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			delta_time = self.clock.tick(FPS) / 1000.0
			self.screen.fill('black')
<<<<<<< HEAD
			self.level.run()
=======
			self.level.run(delta_time)
>>>>>>> 03df69a03265a2e25cdfdb1e5a8f867c9fae577d

			pygame.display.update()


if __name__ == '__main__':
	game = Game()
	game.run()