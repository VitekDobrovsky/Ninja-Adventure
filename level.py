import pygame
from settings import *
from tile import Tile
from tile import Baricade
from player import Player
from support import import_csv_layout
from support import debug
from enemy import Enemy


class Level:
	def __init__(self):
		# define screen
		self.screen = pygame.display.get_surface()

		# groups
		self.visible_sprites = Camera()
		self.obstacle_sprites = pygame.sprite.Group()

		# trap
		self.baricades = {
			'middle': {
				'horizontal': [],
				'vertical': []},
			'left': [],
			'right': [],
			'up': []
		}

		self.traped1 = False
		self.traped2 = False
		self.traped3 = False
		self.traped4 = False
		self.baricades_sprites = []
		self.clear = True

		# create map
		self.layouts = {
			'entities': import_csv_layout('graphics/levels/level_1/CSV_files/1_entities.csv'),
			'border': import_csv_layout('graphics/levels/level_1/CSV_files/1_border.csv'),
			'border_bridge': import_csv_layout('graphics/levels/level_1/CSV_files/1_border_bridge.csv'),			
			'border_corner': import_csv_layout('graphics/levels/level_1/CSV_files/1_border_corner.csv'),			
			'border_horizontal': import_csv_layout('graphics/levels/level_1/CSV_files/1_border_horizontal.csv'),			
			'border_banister': import_csv_layout('graphics/levels/level_1/CSV_files/1_border_banister.csv'),
			'baricades': import_csv_layout('graphics/levels/level_1/CSV_files/1_baricade.csv'),			
			'grass': import_csv_layout('graphics/levels/level_1/CSV_files/1_grass.csv'),
			'trees': import_csv_layout('graphics/levels/level_1/CSV_files/1_tree.csv'),
			}

		self.create_map()	

	def create_map(self):
		# drawing map
		for style,layout in self.layouts.items():
			for row_index,row in enumerate(layout):
				for col_index,col in enumerate(row):
					if col != '-1':
						x = col_index * TILESIZE
						y = row_index * TILESIZE

						if style == 'border':
							Tile((x,y), [self.obstacle_sprites], 'border')
						elif style == 'border_bridge':
							Tile((x,y), [self.obstacle_sprites], 'border_bridge')
						elif style == 'border_corner':
							Tile((x,y), [self.obstacle_sprites], 'border_corner')
						elif style == 'border_horizontal':
							Tile((x,y), [ self.obstacle_sprites], 'border_horizontal')
						elif style == 'border_banister':
							Tile((x,y), [ self.obstacle_sprites], 'border_banister')
						elif style == 'baricades':
							if col == '0':
								self.baricades['middle']['vertical'].append((x,y))
							elif col == '1':
								self.baricades['middle']['horizontal'].append((x,y))
							elif col == '2':
								self.baricades['left'].append((x,y))
							elif col == '3':
								self.baricades['right'].append((x,y))
							elif col == '4':
								self.baricades['up'].append((x,y))

						elif style == 'entities':
							if col == '394':
								self.player = Player((x,y), [self.visible_sprites], self.obstacle_sprites, self.visible_sprites)
							elif col == '390':
								Enemy((x,y), [self.visible_sprites], 'Bamboo')
							elif col == '391':
								Enemy((x,y), [self.visible_sprites], 'Spirit_fire')
							elif col == '392':
								Enemy((x,y), [ self.visible_sprites], 'Racoon')
							elif col == '395':
								Enemy((x,y), [ self.visible_sprites], 'Reptile')

						elif style == 'grass':
							Tile((x,y), [self.visible_sprites], 'grass')
						elif style == 'trees':
							if col == '0' or col == '1':
								Tile((x,y), [self.visible_sprites, self.obstacle_sprites], 'stubbe')
							else:
								Tile((x,y), [self.visible_sprites, self.obstacle_sprites], 'tree')

	def get_island(self):
		current = 'start'

		if self.player.hitbox.y < 2204 and self.player.hitbox.y > 924:
			if self.player.hitbox.x < 3388 and self.player.hitbox.x > 1608:
				current = 'middle'
		elif self.player.hitbox.y < 924:
			current = 'top'
		
		if self.player.hitbox.x > 3388:
			current = 'right'
		elif self.player.hitbox.x < 1608:
			current = 'left'

		return current

	def trap_in_level(self):
		current = self.get_island()
		
		if current == 'middle' and not self.traped1:
			# middle baricades
			bar1 = Baricade(self.baricades['middle']['vertical'][0], [self.visible_sprites, self.obstacle_sprites], 'baricade_vertical', 'middle')
			bar2 = Baricade(self.baricades['middle']['vertical'][1], [self.visible_sprites, self.obstacle_sprites], 'baricade_vertical', 'middle')
			bar3 = Baricade(self.baricades['middle']['horizontal'][0], [self.visible_sprites, self.obstacle_sprites], 'baricade_horizontal', 'middle')
			bar4 = Baricade(self.baricades['middle']['horizontal'][1], [self.visible_sprites, self.obstacle_sprites], 'baricade_horizontal', 'middle')
			
			self.baricades_sprites.append(bar1)
			self.baricades_sprites.append(bar2)
			self.baricades_sprites.append(bar3)
			self.baricades_sprites.append(bar4)
			
			self.traped1 = True
			self.clear = False

		elif current == 'top' and not self.traped2:
			# top baricades
			bar5 = Baricade(self.baricades['up'][0], [self.visible_sprites, self.obstacle_sprites], 'baricade_horizontal', 'top')
			self.baricades_sprites.append(bar5)
			
			self.traped2 = True
			self.clear = False

		elif current == 'left' and not self.traped3:
			# left baricades
			bar6 = Baricade(self.baricades['left'][0], [self.visible_sprites, self.obstacle_sprites], 'baricade_vertical', 'left')
			self.baricades_sprites.append(bar6)
			
			self.traped3 = True
			self.clear = False

		elif current == 'right' and not self.traped4:
			# right baricades
			bar7 = Baricade(self.baricades['right'][0], [self.visible_sprites, self.obstacle_sprites], 'baricade_vertical', 'right')
			self.baricades_sprites.append(bar7)
			
			self.traped4 = True
			self.clear = False

		# removing baricades
		for baricade in self.baricades_sprites:
			baricade.check(current, self.clear)

	def support_keys(self):
		# clear after r
		keys = pygame.key.get_pressed()

		if keys[pygame.K_r]:
			self.clear = True

	def run(self):
		self.visible_sprites.custom_draw(self.player)
		self.visible_sprites.update()
		self.support_keys()
		self.trap_in_level()

class Camera(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		# define screen
		self.screen = pygame.display.get_surface()

		# offset
		self.offset = pygame.math.Vector2()
		self.half_w = self.screen.get_size()[0] // 2
		self.half_h = self.screen.get_size()[1] // 2

		# drawing map
		self.map = pygame.image.load('graphics/levels/level_1/level_1.png').convert_alpha()
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
