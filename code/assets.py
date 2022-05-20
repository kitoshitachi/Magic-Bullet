from dataclasses import dataclass, field
from typing import Tuple
import pygame

from settings import *

@dataclass
class MovingImages:
	up_move: Tuple[pygame.Surface]
	down_move: Tuple[pygame.Surface]
	left_move: Tuple[pygame.Surface]
	right_move: Tuple[pygame.Surface]
	up_left_move: Tuple[pygame.Surface]
	up_right_move: Tuple[pygame.Surface]
	down_left_move: Tuple[pygame.Surface]
	down_right_move: Tuple[pygame.Surface]
	
	up_idle: Tuple[pygame.Surface]
	down_idle: Tuple[pygame.Surface]
	left_idle: Tuple[pygame.Surface]
	right_idle: Tuple[pygame.Surface]
	up_left_idle: Tuple[pygame.Surface]
	up_right_idle: Tuple[pygame.Surface]
	down_left_idle: Tuple[pygame.Surface]
	down_right_idle: Tuple[pygame.Surface]

	_move_sequences: Tuple[Tuple[pygame.Surface]] = field(init=False)
	_idle_sequences: Tuple[Tuple[pygame.Surface]] = field(init=False)

	def __post_init__(self):
		self._move_sequences = (
			self.right_move, 
			self.down_right_move, 
			self.down_move, 
			self.down_left_move, 
			self.left_move, 
			self.up_left_move, 
			self.up_move, 
			self.up_right_move
		)
		
		self._idle_sequences = (
			self.right_idle, 
			self.down_right_idle, 
			self.down_idle, 
			self.down_left_idle, 
			self.left_idle, 
			self.up_left_idle, 
			self.up_idle, 
			self.up_right_idle
		)

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

	def move_squence(self, angle):
		return self._from_angle(angle, self._move_sequences)

	def idle_sequence(self, angle):
		return self._from_angle(angle, self._idle_sequences)


def create_circle_image():
	radius = 32
	width = 1
	surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
	pygame.draw.circle(surface, WHITE, (radius, radius), radius - width, width)
	return surface

pygame.font.init()
pygame.mixer.init()
pygame.display.init()
pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE | pygame.SCALED)

@dataclass
class Assets():
	#font
	font = pygame.font.Font(FONT_PATH, 24)
	font_medium =  pygame.font.Font(FONT_PATH, 32)
	font_large = pygame.font.Font(FONT_PATH, 48)
	
	audio = pygame.mixer.Sound(AUDIO_PATH + "reflect.wav")
	#tileset
	grass_tileset = pygame.image.load(IMAGE_PATH + 'tilesets/pipoya_grass.png').convert_alpha()
	water_tileset = pygame.image.load(IMAGE_PATH + 'tilesets/pipoya_water.png').convert_alpha()
	chip_tileset = pygame.image.load(IMAGE_PATH + 'tilesets/pipoya_chip.png').convert_alpha()
	#image
	circle = create_circle_image()
	arrow = pygame.image.load(IMAGE_PATH + 'player/arrow.png').convert_alpha()
	smoke_effect = [pygame.image.load(f"{IMAGE_PATH}/smoke_effect/{i}.png").convert_alpha() for i in range(7)]
	frog_img = pygame.image.load(IMAGE_PATH + 'NPC/frog.png').convert_alpha()
	bullet_img = pygame.image.load(IMAGE_PATH + 'player/Bullet.png').convert_alpha()
	arrow_img = pygame.image.load(IMAGE_PATH + 'player/arrow.png').convert_alpha()
	player1_img = pygame.image.load(IMAGE_PATH + 'player/player1.png').convert_alpha()
	player2_img = pygame.image.load(IMAGE_PATH + 'player/player2.png').convert_alpha()

	player1: MovingImages = field(init=False)
	player2: MovingImages = field(init=False)
	frog: MovingImages = field(init=False)

	def __post_init__(self):
		Assets.player1 = MovingImages(
			*(Assets._create_animation_sprites(Assets.player1_img, i, 2, (30, 50)) for i in range(8)),
			Assets._create_animation_sprites(Assets.player1_img, 8, 1, (30, 50)),
			*(Assets._create_animation_sprites(Assets.player1_img, i, 2, (30, 50)) for i in range(9, 12)),
			*(Assets._create_animation_sprites(Assets.player1_img, i, 1, (30, 50)) for i in range(12, 14)),
			*(Assets._create_animation_sprites(Assets.player1_img, i, 2, (30, 50)) for i in range(14, 16))
			)

		Assets.player2 = MovingImages(
			*(Assets._create_animation_sprites(Assets.player2_img, i, 2, (30, 50)) for i in range(8)),
			Assets._create_animation_sprites(Assets.player2_img, 8, 1, (30, 50)),
			*(Assets._create_animation_sprites(Assets.player2_img, i, 2, (30, 50)) for i in range(9, 12)),
			*(Assets._create_animation_sprites(Assets.player2_img, i, 1, (30, 50)) for i in range(12, 14)),
			*(Assets._create_animation_sprites(Assets.player2_img, i, 2, (30, 50)) for i in range(14, 16))
		)

		Assets.frog = MovingImages(
			*(Assets._create_animation_sprites(Assets.frog_img, i, 2, (32, 32)) for i in range(8)),
			*(Assets._create_animation_sprites(Assets.frog_img, i, 1, (32, 32)) for i in range(8, 16))
		)

	@staticmethod
	def _create_animation_sprites(src, row, amount, sprite_size):
		sprites = ()
		for i in range(amount):
			img = pygame.Surface(sprite_size, pygame.SRCALPHA)
			img.blit(src, (0, 0), (i * sprite_size[0], row * sprite_size[1], *sprite_size))
			sprites += (img,)

		return sprites