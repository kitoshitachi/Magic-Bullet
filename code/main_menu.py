import pygame
import pygame_menu
from assets import Assets
from settings import *

from settings import *

class MainMenu:
	def __init__(self, on_start_game, surface):
		'''
		make main menu

		param on_start_game: events
		param surface: surface to draw main menu
		'''
		button_color = pygame.Color(MENU_LIGHT_GREEN)
		border_color = pygame.Color(MENU_DARK_GREEN)
		selection_color = pygame.Color(MENU_BLUE)

		theme = pygame_menu.themes.THEME_BLUE.copy()
		theme.background_color = pygame_menu.BaseImage(
			IMAGE_PATH + "menu/main_menu_bg.png", pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY
		)
		theme.title_background_color = border_color

		theme.title_bar_style = pygame_menu.widgets.pygame_menu.widgets.MENUBAR_STYLE_NONE
		theme.widget_selection_effect = pygame_menu.widgets.LeftArrowSelection()
		theme.widget_font = Assets.font
		theme.title_font = Assets.font_large
		theme.title_font_color = button_color
		theme.title_font_shadow_color = border_color
		theme.title_font_shadow_offset = 7
		theme.title_font_shadow_position = pygame_menu.locals.POSITION_SOUTHEAST
		theme.title_offset = (SCREEN_WIDTH/2 - 175, SCREEN_HEIGHT/2 - 170)

		self._menu = pygame_menu.Menu('Magic Bullet', *surface.get_size(), theme=theme)

		button_style = {
			"background_color": button_color,
			"background_inflate": (100, 10),
			"border_width": 3,
			"border_color": border_color,
			"font_color": border_color,
			"selection_color": selection_color,
		}

		self._menu.add.button('Chơi', on_start_game, margin=(0, 30), **button_style)
		self._menu.add.button('Thoát', pygame_menu.events.EXIT, **button_style)

		self._surface = surface

	def run(self, events):
		'''
		params events: handle event to run
		
		'''
		self._menu.update(events)
		self._menu.draw(self._surface)

	def reset(self):
		'''reset menu'''
		self.menu.reset()
