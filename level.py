import pygame
from settings import *
from tile import Tile
from player import Player


class Level:
	def __init__(self):
		# set up
		self.screen = pygame.display.get_surface()
		self.visible_sprites = Camera()
		self.obstacle_sprites = pygame.sprite.Group()

		# create map
		self.create_map()

	def create_map(self):
		for row_index,row in enumerate(WORLD_MAP):
			for col_index,col in enumerate(row):
				x = col_index * TILESIZE
				y = row_index * TILESIZE
				if col == 'x':
					Tile((x,y),[self.visible_sprites, self.obstacle_sprites])
				elif col == 'p':
					self.player = Player((x,y), [self.visible_sprites], self.obstacle_sprites)

	def run(self):
		self.visible_sprites.custom_draw(self.player)
		self.visible_sprites.update()


class Camera(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.screen = pygame.display.get_surface()

		# offset
		self.offset = pygame.math.Vector2()
		self.half_w = self.screen.get_size()[0] // 2
		self.half_h = self.screen.get_size()[1] // 2

	def custom_draw(self, player):
		self.offset.x = player.rect.centerx - self.half_w
		self.offset.y = player.rect.centery - self.half_h

		for sprite in self.sprites():
			pos_offset = sprite.rect.topleft - self.offset
			self.screen.blit(sprite.image, pos_offset)
