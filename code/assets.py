from dataclasses import dataclass, field
from typing import List
import pygame

from settings import TILESIZE, WHITE

@dataclass
class MovingImages:
		up_move: List[pygame.Surface]
		down_move: List[pygame.Surface]
		left_move: List[pygame.Surface]
		right_move: List[pygame.Surface]
		up_left_move: List[pygame.Surface]
		up_right_move: List[pygame.Surface]
		down_left_move: List[pygame.Surface]
		down_right_move: List[pygame.Surface]
		up_idle: List[pygame.Surface]
		down_idle: List[pygame.Surface]
		left_idle: List[pygame.Surface]
		right_idle: List[pygame.Surface]
		up_left_idle: List[pygame.Surface]
		up_right_idle: List[pygame.Surface]
		down_left_idle: List[pygame.Surface]
		down_right_idle: List[pygame.Surface]

		_move_sequences: List[List[pygame.Surface]] = field(init=False)
		_idle_sequences: List[List[pygame.Surface]] = field(init=False)

		def __post_init__(self):
			self._move_sequences = [self.right_move, self.down_right_move, self.down_move, self.down_left_move, self.left_move, self.up_left_move, self.up_move, self.up_right_move]
			self._idle_sequences = [self.right_idle, self.down_right_idle, self.down_idle, self.down_left_idle, self.left_idle, self.up_left_idle, self.up_idle, self.up_right_idle]

		def _from_angle(self, angle, sequences):
			if angle < 0:
				angle += 360

			if angle > 337.5 or angle <= 22.5:
				return sequences[0]
			if angle <= 67.5:
				return sequences[1]
			elif angle <= 112.5:
				return sequences[2]
			elif angle <= 157.5:
				return sequences[3]
			elif angle <= 202.5:
				return sequences[4]
			elif angle <= 247.5:
				return sequences[5]
			elif angle <= 292.5:
				return sequences[6]
			else:
				return sequences[7]

		def get_move_sequence_from_angle(self, angle) -> List[pygame.Surface]:
			return self._from_angle(angle, self._move_sequences)

		def get_idle_sequence_from_angle(self, angle) -> List[pygame.Surface]:
			return self._from_angle(angle, self._idle_sequences)


class Assets():
	font: pygame.font.Font = None
	font_large: pygame.font.Font = None
	grass_tileset: pygame.Surface = None
	water_tileset : pygame.Surface = None
	chip_tileset: pygame.Surface = None
	arrow: pygame.Surface = None
	circle: pygame.Surface = None
	smoke_effect: pygame.Surface = None
	player1: MovingImages = None
	frog: MovingImages = None

	def init():
		Assets.font = pygame.font.Font("graphics/font/FVF Fernando 08.ttf", 24)
		Assets.font_large = pygame.font.Font("graphics/font/FVF Fernando 08.ttf", 48)

		Assets.grass_tileset = pygame.image.load('graphics/pipoya_grass.png').convert_alpha()
		Assets.water_tileset = pygame.image.load('graphics/pipoya_water.png').convert_alpha()
		Assets.chip_tileset = pygame.image.load('graphics/pipoya_chip.png').convert_alpha()
		Assets.bullet = pygame.image.load('graphics/test/BulletProjectile.png').convert_alpha()
		Assets.arrow = pygame.image.load('graphics/arrow.png').convert_alpha()
		Assets.circle = Assets.create_circle_image()
		Assets.smoke_effect = [pygame.image.load(f"./graphics/smoke_effect/{i}.png").convert_alpha() for i in range(7)]
		frog_img = pygame.image.load('graphics/NPC/frog.png').convert_alpha()
		player1_img = pygame.image.load('graphics/player1.png').convert_alpha()

		Assets.player1 = MovingImages(
			*(Assets._create_animation_sprites(player1_img, i, 2, (30, 50)) for i in range(8)),
			Assets._create_animation_sprites(player1_img, 8, 1, (30, 50)),
			*(Assets._create_animation_sprites(player1_img, i, 2, (30, 50)) for i in range(9, 12)),
			*(Assets._create_animation_sprites(player1_img, i, 1, (30, 50)) for i in range(12, 14)),
			*(Assets._create_animation_sprites(player1_img, i, 2, (30, 50)) for i in range(14, 16))
			)
		Assets.frog = MovingImages(
			*(Assets._create_animation_sprites(frog_img, i, 2, (32, 32)) for i in range(8)),
			*(Assets._create_animation_sprites(frog_img, i, 1, (32, 32)) for i in range(8, 16))
		)

	def _create_animation_sprites(src, row, amount, sprite_size) -> pygame.Surface:
		sprites = []
		for i in range(amount):
			img = pygame.Surface(sprite_size, pygame.SRCALPHA)
			img.blit(src, (0, 0), (i * sprite_size[0], row * sprite_size[1], *sprite_size))
			sprites.append(img)

		return sprites

	def create_circle_image():
		radius = 32
		width = 1
		surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
		pygame.draw.circle(surface, WHITE, (radius, radius), radius - width, width)
		return surface
