import pygame

from settings import SCREEN_HEIGHT, SCREEN_WIDTH
pygame.init()
font = pygame.font.Font(None,30)

debug_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

def debug(info,y = 10, x = 10):
	display_surface = pygame.display.get_surface()
	debug_surf = font.render(str(info),True,'White')
	debug_rect = debug_surf.get_rect(topleft = (x,y))
	pygame.draw.rect(display_surface,'Black',debug_rect)
	display_surface.blit(debug_surf,debug_rect)

def get_debug_surface():
	return debug_surface