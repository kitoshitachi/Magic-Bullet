import pygame
import pygame_menu
from assets import Assets
from settings import MENU_PAUSE_BG

from settings import *


class PauseMenu:
	def __init__(self, on_start_game, on_main_menu, surface):
		'''
		create pause menu

		params on_start_game: status of game
		params on_main_menu: event
		params surface: surface to draw menu
		'''
		self._pause_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
		self._screen_shot = None
		button_color = pygame.Color(MENU_LIGHT_GREEN)
		border_color = pygame.Color(MENU_DARK_GREEN)
		selection_color = pygame.Color(MENU_BLUE)

		theme = pygame_menu.themes.THEME_BLUE.copy()
		theme.background_color = pygame.Color(MENU_PAUSE_BG)
		theme.title_background_color = border_color
		theme.title_bar_style = pygame_menu.widgets.pygame_menu.widgets.MENUBAR_STYLE_NONE
		theme.widget_selection_effect = pygame_menu.widgets.LeftArrowSelection()
		theme.widget_font = Assets.font
		theme.title_font = Assets.font_large
		theme.title_font_color = button_color
		theme.title_font_shadow_color = border_color
		theme.title_font_shadow_offset = 7
		theme.title_font_shadow_position = pygame_menu.locals.POSITION_SOUTHEAST

		theme.title_offset = (SCREEN_WIDTH/2 - 120, SCREEN_HEIGHT/2 - 200)

		self._menu = pygame_menu.Menu('PAUSED', *surface.get_size(), theme=theme)

		button_style = {
			"background_color": button_color,
			"background_inflate": (100, 10),
			"border_width": 3,
			"border_color": border_color,
			"font_color": border_color,
			"selection_color": selection_color,
		}
		self._first_widget = self._menu.add.button('Chơi', on_start_game, margin=(0, 30), **button_style)
		self._menu.add.button('Về màn hình chính', on_main_menu, margin=(0, 30), **button_style)
		self._menu.add.button('Thoát', pygame_menu.events.EXIT, **button_style)

		self._surface = surface

	def run(self, events):
		'''
		params events: handle event and run
		'''
		self._menu.update(events)
		
		self._pause_surface.fill(color=TRANSPARENT)
		self._menu.draw(self._pause_surface)

		self._surface.blit(self._screen_shot, (0, 0))
		self._surface.blit(self._pause_surface, (0, 0))

	def take_screen_shot(self):
		'''create copy screen shot'''
		self._screen_shot = self._surface.copy()

	def reset(self):
		'''reset menu'''
		self._menu.full_reset()
		self._menu.select_widget(self._first_widget)
