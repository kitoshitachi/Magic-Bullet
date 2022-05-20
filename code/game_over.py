import pygame
import pygame_menu
from assets import Assets
from settings import *


class GameOver:
	def __init__(self, on_main_menu, surface, playerName):
		self.pause_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
		self.screen_shot = None
		button_color = pygame.Color(MENU_LIGHT_GREEN)
		border_color = pygame.Color(MENU_DARK_GREEN)
		selection_color = pygame.Color(MENU_BLUE)

		theme = pygame_menu.themes.THEME_BLUE.copy()
		theme.background_color = pygame.Color(MENU_PAUSE_BG)
		theme.title_background_color = border_color
		theme.title_bar_style = pygame_menu.widgets.pygame_menu.widgets.MENUBAR_STYLE_NONE
		theme.widget_selection_effect = pygame_menu.widgets.LeftArrowSelection()
		theme.widget_font = Assets.font
		theme.title_font = Assets.font_medium
		theme.title_font_color = button_color
		theme.title_font_shadow_color = border_color
		theme.title_font_shadow_offset = 7
		theme.title_font_shadow_position = pygame_menu.locals.POSITION_SOUTHEAST

		theme.title_offset = (130, SCREEN_HEIGHT/2 - 200)

		menu = pygame_menu.Menu(f'Người chơi {playerName} {"(bên trái)" if playerName == 1 else "(bên phải)"} chiến thắng!', *surface.get_size(), theme=theme)

		button_style = {
			"background_color": button_color,
			"background_inflate": (100, 10),
			"border_width": 3,
			"border_color": border_color,
			"font_color": border_color,
			"selection_color": selection_color,
		}

		menu.add.image(IMAGE_PATH + ("menu/player1_win.png" if playerName == 1 else "menu/player2_win.png"), margin=(0, 10))
		self.first_widget = menu.add.button('Về màn hình chính', on_main_menu, margin=(0, 30), **button_style)
		menu.add.button('Thoát', pygame_menu.events.EXIT, **button_style)


		self.menu = menu
		self.surface = surface

	def run(self, events):
		self.menu.update(events)

		self.pause_surface.fill(color=TRANSPARENT)
		self.menu.draw(self.pause_surface)

		self.surface.blit(self.screen_shot, (0, 0))
		self.surface.blit(self.pause_surface, (0, 0))

	def take_screen_shot(self):
		self.screen_shot = self.surface.copy()

	def reset(self):
		self.menu.full_reset()
		self.menu.select_widget(self.first_widget)
