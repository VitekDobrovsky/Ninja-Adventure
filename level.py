import pygame
from settings import *
from tile import Tile
from tile import Baricade
from player import Player
from support import *
from enemy import Enemy, Dead_enemy
from random import randint
from gui import GUI
from chest import Chest 


class Level:
	def __init__(self):
		# define screen
		self.screen = pygame.display.get_surface()

		# groups
		self.visible_sprites = Camera()
		self.obstacle_sprites = pygame.sprite.Group()
		self.enemy = pygame.sprite.Group()
		self.chests_group = pygame.sprite.Group()

		# trap on isand
		self.baricades = {
			'middle': [],
			'left': [],
			'right': [],
			'up': []
		}

		self.traped1 = False
		self.traped2 = False
		self.traped3 = False
		self.traped4 = False
		self.baricades_sprites = []
		self.baricade_time = None
		self.baricade_an_index = 0
		self.clear = True

		# enemy
		self.enemy_speed_index = 1
		self.enemies = {
			'middle': {
				'Racoon' : [],
				'Bamboo': []
			},

			'top': {
				'Racoon': [],
				'Spirit_fire': []
			},

			'right': {
				'Reptile': [],
				'Bamboo': []
			},

			'left': {
				'Racoon': [],
				'Reptile': []
			}
		}
		self.dead_enemies = { 
			'Racoon': [],
			'Bamboo': [],
			'Spirit_fire': [],
			'Reptile': []
		}

		# enemy damage
		self.enemy_count = 0

		# 'CLEAR' text
		self.text1 = Text(self.screen, 'CLEAR', 'graphics/fonts/game.ttf', 100, (WIDTH/2, HEIGHT/3), 'black'), Text(self.screen, 'clear', 'graphics/fonts/game.ttf', 120, (WIDTH/2, HEIGHT/3), RED_TEXT)
		self.c = Text(self.screen, 'C', 'graphics/fonts/game.ttf', 80, (WIDTH/2 - 138, HEIGHT/3), RED_TEXT)
		self.l = Text(self.screen, 'L', 'graphics/fonts/game.ttf', 80, (WIDTH/2 - 69, HEIGHT/3), RED_TEXT)
		self.e = Text(self.screen, 'E', 'graphics/fonts/game.ttf', 80, (WIDTH/2, HEIGHT/3), RED_TEXT)
		self.a = Text(self.screen, 'A', 'graphics/fonts/game.ttf', 80, (WIDTH/2 + 68, HEIGHT/3), RED_TEXT)
		self.r = Text(self.screen, 'R', 'graphics/fonts/game.ttf', 80, (WIDTH/2 + 136, HEIGHT/3), RED_TEXT)			
		
		self.text1[0].text_surf.set_alpha(0)
		self.text1[1].text_surf.set_alpha(0)
		self.c.text_surf.set_alpha(0)
		self.l.text_surf.set_alpha(0)
		self.e.text_surf.set_alpha(0)
		self.a.text_surf.set_alpha(0)
		self.r.text_surf.set_alpha(0)
		
		self.al = 0
		self.clear_tm = 0

		# chests
		self.chests = {
			'middle' : None,
			'left': None,
			'right': None,
			'top': None
		} 

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
			'chests': import_csv_layout('graphics/levels/level_1/CSV_files/1_chest.csv')
			}

		self.create_map()	

		# GUI
		self.gui = GUI(self.player)

	# MAP
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
								self.baricades['middle'].append((x,y))
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
								self.sort_enemy(x, y, 'Bamboo')
							elif col == '391':
								self.sort_enemy(x, y, 'Spirit_fire')
							elif col == '392':
								self.sort_enemy(x, y, 'Racoon')
							elif col == '395':
								self.sort_enemy(x, y, 'Reptile')

						elif style == 'grass':
							Tile((x,y), [self.visible_sprites], 'grass')
						elif style == 'trees':
							if col == '0' or col == '1':
								Tile((x,y), [self.visible_sprites, self.obstacle_sprites], 'stubbe')
							else:
								Tile((x,y), [self.visible_sprites, self.obstacle_sprites], 'tree')
						elif style == 'chests':
							if col == '0':
								# middle
								self.chests['middle'] = (x,y)
							elif col == '1':
								# right
								self.chests['right'] = (x,y)
							elif col == '2':
								# left
								self.chests['left'] = (x,y)
							elif col == '3':
								# top
								self.chests['top'] = (x,y)

	def get_island(self):
		current = 'start'

		if self.is_middle(self.player.hitbox.x, self.player.hitbox.y):
			current = 'middle'
		elif self.is_top(self.player.hitbox.y):
			current = 'top'
		
		if self.is_right(self.player.hitbox.x):
			current = 'right'
		elif self.is_left(self.player.hitbox.x):
			current = 'left'

		elif self.player.hitbox.y > 2203:
			current = 'start'

		return current

	def trap_in_level(self):
		current = self.get_island()
		
		if current == 'middle' and not self.traped1:
			# middle baricades
			index = 0 
			for i in self.baricades['middle']:
				Baricade(self.baricades['middle'][index], [self.visible_sprites, self.obstacle_sprites], self.baricades_sprites, 'middle')
				index += 1
			
			# enemies set up for island
			self.spawn_enemies()
			self.count_enemies()

			self.traped1 = True
			self.clear = False
			self.baricade_time = pygame.time.get_ticks()

		elif current == 'top' and not self.traped2:
			# top baricades
			index = 0
			for i in self.baricades['up']:
				Baricade(self.baricades['up'][index], [self.visible_sprites, self.obstacle_sprites], self.baricades_sprites, 'top')
				index += 1
			
			# enemies set up for island
			self.spawn_enemies()
			self.count_enemies()

			self.traped2 = True
			self.clear = False
			self.baricade_time = pygame.time.get_ticks()

		elif current == 'left' and not self.traped3:
			# left baricades
			index = 0
			for i in self.baricades['left']:
				Baricade(self.baricades['left'][index], [self.visible_sprites, self.obstacle_sprites], self.baricades_sprites, 'left')
				index += 1
			
			# enemies set up for island
			self.spawn_enemies()
			self.count_enemies()

			self.traped3 = True
			self.clear = False
			self.baricade_time = pygame.time.get_ticks()

		elif current == 'right' and not self.traped4:
			# right baricades
			index = 0
			for i in self.baricades['right']:
				Baricade(self.baricades['right'][index], [self.visible_sprites, self.obstacle_sprites], self.baricades_sprites, 'right')
				index += 1
			
			# enemies set up for island
			self.spawn_enemies()
			self.count_enemies()

			self.traped4 = True
			self.clear = False
			self.baricade_time = pygame.time.get_ticks()

	def baricade_animations(self):
		current = self.get_island()
		index = 0.005

		for baricade in self.baricades_sprites:
				
			if self.baricade_an_index <= 3.9 and not self.clear:
				self.baricade_an_index += index

			if self.clear and self.baricade_an_index >= 0:
				self.baricade_an_index -= index

			if self.baricade_an_index <= 0:
				baricade.kill()

			baricade.image = baricade.frames[int(self.baricade_an_index)]

	def create_chests(self):
		current = self.get_island()

		if self.clear_tm == 1 and current != 'start':
			pos = self.chests[current]
			Chest(pos,[self.visible_sprites, self.obstacle_sprites, self.chests_group], self.player, self.screen, self.visible_sprites)


	# ENEMIES
	def sort_enemy(self, x, y, type):
		# enemy sorting to enemy lists 
		if self.is_middle(x, y):
			self.enemies['middle'][type].append((x,y))

		elif self.is_top(y):
			self.enemies['top'][type].append((x,y))

		elif self.is_left(x):
			self.enemies['left'][type].append((x,y))

		elif self.is_right(x):
			self.enemies['right'][type].append((x,y))

	def count_enemies(self):
		for enemy in self.enemy.sprites():
			self.enemy_count += 1

	def spawn_enemies(self):
		# current island
		current = self.get_island()

		# middle enemies
		if current == 'middle':
			index = 0
			for g in range(3):
				pos = self.enemies['middle']['Bamboo'][index]
				Enemy(pos, [self.visible_sprites, self.enemy], 'Bamboo', self.obstacle_sprites, self.player, self.enemy_speed_index)
				self.enemy_speed_index += 0.5
				index += 1

			index = 0
			for l in range(2):
				pos = self.enemies['middle']['Racoon'][index]
				Enemy(pos, [self.visible_sprites, self.enemy], 'Racoon', self.obstacle_sprites, self.player, self.enemy_speed_index)
				self.enemy_speed_index += 0.5
				index += 1
				
			self.traped1 = False
			self.enemy_speed_index = 1


		# top enemies
		if current == 'top':
			index = 0
			for a in range(2):
				pos = self.enemies['top']['Racoon'][index]
				Enemy(pos, [self.visible_sprites, self.enemy], 'Racoon', self.obstacle_sprites, self.player, self.enemy_speed_index)
				self.enemy_speed_index += 0.5
				index += 1

			index = 0
			for b in range(3):
				pos = self.enemies['top']['Spirit_fire'][index]
				Enemy(pos, [self.visible_sprites, self.enemy], 'Spirit_fire', self.obstacle_sprites, self.player, self.enemy_speed_index)
				self.enemy_speed_index += 0.5
				index += 1

			self.traped2 = False
			self.enemy_speed_index = 1

		# left enemies
		if current == 'left':
			index = 0
			for c in range(2):
				pos = self.enemies['left']['Racoon'][index]
				Enemy(pos, [self.visible_sprites, self.enemy], 'Racoon', self.obstacle_sprites, self.player, self.enemy_speed_index)
				self.enemy_speed_index += 0.5
				self.enemy_speed_index = 1
				index += 1

			index = 0
			for d in range(3):
				pos = self.enemies['left']['Reptile'][index]
				Enemy(pos, [self.visible_sprites, self.enemy], 'Reptile', self.obstacle_sprites, self.player, self.enemy_speed_index)
				self.enemy_speed_index += 0.5
				index += 1

			self.traped3 = False
			self.enemy_speed_index = 1

		# right enemies
		if current == 'right':
			index = 0
			for e in range(2):
				pos = self.enemies['right']['Bamboo'][index]
				Enemy(pos, [self.visible_sprites, self.enemy], 'Bamboo', self.obstacle_sprites, self.player, self.enemy_speed_index)
				self.enemy_speed_index += 0.5
				index += 1

			index = 0
			for f in range(3):
				pos = self.enemies['right']['Reptile'][index]
				Enemy(pos, [self.visible_sprites, self.enemy], 'Reptile', self.obstacle_sprites, self.player, self.enemy_speed_index)
				self.enemy_speed_index += 0.5
				index += 1 

			index = 0
			self.traped4 = False
			self.enemy_speed_index = 1

	def kill_enemy(self):
		# kill enemy
		for enemy in self.enemy:
			if enemy.health <= 0:
				self.dead_enemies[enemy.type].append((enemy.hitbox.x,enemy.hitbox.y))
				Dead_enemy((enemy.hitbox.x, enemy.hitbox.y), [self.visible_sprites], enemy.type)
				enemy.kill()
				self.enemy_count -= 1

	def kill_all(self):
		self.enemy_count = 0
		for enemy in self.enemy:
			enemy.kill()

	# PLAYER
	def damage_player(self):
		for enemy in self.enemy.sprites():
			if enemy.can_attack and self.player.vulnerable and enemy.direction == (0,0):
				self.player.health -= ENEMY_DAMAGE[enemy.type]
				self.player.vulnerable = False
				self.player.damage_time = pygame.time.get_ticks()

	def draw_gui(self):
		if self.show_map:
			self.gui.map()
		else:
			self.gui.display_stats()

	# SUPPORT
	def input(self):
		keys = pygame.key.get_pressed()

		# show map
		if keys[pygame.K_m]:
			self.show_map = True
		else:
			self.show_map = False

		# kill all on G
		if keys[pygame.K_g]:
			self.kill_all()

	def is_middle(self, x, y):
		if y < 2204 and y > 924:
			if x < 3388 and x > 1608:
				return True

	def is_left(self, x):
		if x < 1608:
			return True 

	def is_right(self,x):
		if x > 3388:
			return True

	def is_top(self, y):
		if y < 924:
			return True

	def clear_text(self):
		if self.al >= 0:
			self.al -= 5
		
		self.c.draw()
		self.l.draw()
		self.e.draw()
		self.a.draw()
		self.r.draw()
		draw_surface(self.screen, WIDTH/2 - 159,HEIGHT/3 - 20 ,35,60, RED_TEXT, self.al)
		draw_surface(self.screen, WIDTH/2 - 80,HEIGHT/3 + 10 ,40,10, RED_TEXT, self.al)
		draw_surface(self.screen, WIDTH/2 - 20 ,HEIGHT/3 - 20,35,60, RED_TEXT, self.al)
		draw_surface(self.screen, WIDTH/2 + 50,HEIGHT/3 - 20,30,60, RED_TEXT, self.al)
		draw_surface(self.screen, WIDTH/2 + 110,HEIGHT/3 - 30,40,55, RED_TEXT, self.al)
		self.text1[1].draw()
		self.text1[0].draw()

		self.text1[0].text_surf.set_alpha(self.al)
		self.text1[1].text_surf.set_alpha(self.al)
		self.c.text_surf.set_alpha(self.al)
		self.l.text_surf.set_alpha(self.al)
		self.e.text_surf.set_alpha(self.al)
		self.a.text_surf.set_alpha(self.al)
		self.r.text_surf.set_alpha(self.al)

		if self.clear_tm <= 50 and self.enemy_count == 0 and self.get_island() != 'start':
			self.clear_tm += 1
			self.al = 255
		if self.enemy_count != 0:
			self.clear_tm = 0

	def clear_island(self):
		if self.enemy_count == 0:
			self.clear = True

	# RUN
	def run(self):
		self.visible_sprites.custom_draw(self.player)
		self.visible_sprites.update()
		self.input()
		self.clear_island()
		self.kill_enemy()
		self.damage_player()
		self.baricade_animations()
		self.create_chests()
		self.chests_group.update()
		self.trap_in_level()
		self.draw_gui()
		self.clear_text()

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
