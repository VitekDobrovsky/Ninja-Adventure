import pygame
from settings import *
from tile import Tile
from player import Player
from support import import_csv_layout


class Level:
	def __init__(self):
		# set up
		self.screen = pygame.display.get_surface()
		self.visible_sprites = Camera()
		self.obstacle_sprites = pygame.sprite.Group()

		# create map
		self.layouts = {
			'entities': import_csv_layout('graphics/levels/level_1/CSV_files/1_entities.csv'),
			'boundaries': import_csv_layout('graphics/levels/level_1/CSV_files/1_boundaries.csv'),
			'grass': import_csv_layout('graphics/levels/level_1/CSV_files/1_grass.csv')
			}
		self.create_map()



	def create_map(self):
		for style,layout in self.layouts.items():
			for row_index,row in enumerate(layout):
				for col_index,col in enumerate(row):
					if col != '-1':
						x = col_index * TILESIZE
						y = row_index * TILESIZE

						if style == 'boundaries':
							Tile((x,y), [self.obstacle_sprites], 'border')
						elif style == 'entities':
							self.player = Player((x,y), [self.visible_sprites], self.obstacle_sprites)
						elif style == 'grass':
							Tile((x,y), [self.visible_sprites], 'grass')





					

	def run(self):
		self.visible_sprites.custom_draw(self.player)
		self.visible_sprites.update()


class Camera(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		# getting display surface
		self.screen = pygame.display.get_surface()

		# offset
		self.offset = pygame.math.Vector2()
		self.half_w = self.screen.get_size()[0] // 2
		self.half_h = self.screen.get_size()[1] // 2

		# map
		self.map = pygame.image.load('graphics/levels/level_1/level_1.png')
		self.map_rect = self.map.get_rect(topleft=(0,0))

	def custom_draw(self, player):
		# apply offset
		self.offset.x = player.rect.centerx - self.half_w
		self.offset.y = player.rect.centery - self.half_h

		# drawing map
		map_offset = self.map_rect.topleft - self.offset
		self.screen.blit(self.map, map_offset)

		# drawing sprites
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			pos_offset = sprite.rect.topleft - self.offset
			self.screen.blit(sprite.image, pos_offset)
