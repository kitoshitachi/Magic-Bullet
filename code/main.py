import pygame, sys
from tilesets import Tilesets
from settings import *
from level import Level

class Game:
	def __init__(self):
		  
		# general setup
		pygame.init()
		
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE | pygame.SCALED)
		self.display_surface = pygame.display.get_surface()
		Tilesets.init()

		pygame.image.load('graphics/pipoya_grass.png').convert_alpha()
  
		pygame.display.set_caption('Magic Bullet')
  
		self.clock = pygame.time.Clock()

		self.level = Level('map1')
	
	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			self.screen.fill('black')
			self.level.run()

			pygame.display.update()
			self.clock.tick(FPS)

if __name__ == '__main__':
	game = Game()
	game.run()