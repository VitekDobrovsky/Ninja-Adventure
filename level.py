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

		# clear text		
		self.t_clear_sheet = Sprite_sheet('graphics/GUI/clear_text_sheet.png', (41, 16), (41 * 11, 16 * 9))
		self.t_clear_image = self.t_clear_sheet.get_image(0,0)
		self.t_clear_rect = self.t_clear_image.get_rect(center=(WIDTH / 2, HEIGHT / 4))

		self.t_clear_animate = False
		self.t_clear_index = 0
		self.t_clear_speed = 0.05
		self.t_clear_frames = [self.t_clear_sheet.get_image(0,0), self.t_clear_sheet.get_image(1,0), self.t_clear_sheet.get_image(2,0),
								self.t_clear_sheet.get_image(3,0), self.t_clear_sheet.get_image(4,0)]

		self.clear_tm = 0

		# you died text
		self.death_text_sheet = Sprite_sheet('graphics/GUI/You_died.png', (72, 25), ((72 * 9, 25 * 7)))
		self.death_text_img = self.death_text_sheet.get_image(0,0)
		self.death_text_rect = self.death_text_img.get_rect(center=(WIDTH / 2, HEIGHT / 4))

		self.death_text_index = 0
		self.death_text_speed = 0.05

		self.death_text_frames = [self.death_text_sheet.get_image(0,0), self.death_text_sheet.get_image(1,0), self.death_text_sheet.get_image(2,0), 
			    					self.death_text_sheet.get_image(3,0), self.death_text_sheet.get_image(4,0), ]

		# play again text
		self.font = pygame.font.Font('graphics/fonts/Gameplay.ttf' ,30)
		self.playagain_txt = self.font.render('press space to play again',True, (225,225,225))
		self.playagain_rect = self.playagain_txt.get_rect(midtop=(self.death_text_rect.centerx,self.death_text_rect.y + 200))
		self.playagain_txt.set_alpha(0)
		self.playagain_alpha = 0


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

	def trap_in_level(self, dificulty):
		current = self.get_island()
		
		if current == 'middle' and not self.traped1:
			# middle baricades
			index = 0 
			for i in self.baricades['middle']:
				Baricade(self.baricades['middle'][index], [self.visible_sprites, self.obstacle_sprites], self.baricades_sprites, 'middle')
				index += 1
			
			# enemies set up for island
			self.spawn_enemies(dificulty)
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
			self.spawn_enemies(dificulty)
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
			self.spawn_enemies(dificulty)
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
			self.spawn_enemies(dificulty)
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
			Chest(pos,[self.visible_sprites, self.obstacle_sprites], self.player, self.screen, self.visible_sprites)

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

	def spawn_enemies(self,dificulty):
		# current island
		current = self.get_island()

		# middle enemies
		if current == 'middle':
			index = 0
			for g in range(3):
				pos = self.enemies['middle']['Bamboo'][index]
				Enemy(pos, [self.visible_sprites, self.enemy], 'Bamboo', self.obstacle_sprites, self.player, self.enemy_speed_index, dificulty)
				self.enemy_speed_index += 0.5
				index += 1

			index = 0
			for l in range(2):
				pos = self.enemies['middle']['Racoon'][index]
				Enemy(pos, [self.visible_sprites, self.enemy], 'Racoon', self.obstacle_sprites, self.player, self.enemy_speed_index, dificulty)
				self.enemy_speed_index += 0.5
				index += 1
				
			self.traped1 = False
			self.enemy_speed_index = 1


		# top enemies
		if current == 'top':
			index = 0
			for a in range(2):
				pos = self.enemies['top']['Racoon'][index]
				Enemy(pos, [self.visible_sprites, self.enemy], 'Racoon', self.obstacle_sprites, self.player, self.enemy_speed_index, dificulty)
				self.enemy_speed_index += 0.5
				index += 1

			index = 0
			for b in range(3):
				pos = self.enemies['top']['Spirit_fire'][index]
				Enemy(pos, [self.visible_sprites, self.enemy], 'Spirit_fire', self.obstacle_sprites, self.player, self.enemy_speed_index, dificulty)
				self.enemy_speed_index += 0.5
				index += 1

			self.traped2 = False
			self.enemy_speed_index = 1

		# left enemies
		if current == 'left':
			index = 0
			for c in range(2):
				pos = self.enemies['left']['Racoon'][index]
				Enemy(pos, [self.visible_sprites, self.enemy], 'Racoon', self.obstacle_sprites, self.player, self.enemy_speed_index, dificulty)
				self.enemy_speed_index += 0.5
				self.enemy_speed_index = 1
				index += 1

			index = 0
			for d in range(3):
				pos = self.enemies['left']['Reptile'][index]
				Enemy(pos, [self.visible_sprites, self.enemy], 'Reptile', self.obstacle_sprites, self.player, self.enemy_speed_index, dificulty)
				self.enemy_speed_index += 0.5
				index += 1

			self.traped3 = False
			self.enemy_speed_index = 1

		# right enemies
		if current == 'right':
			index = 0
			for e in range(2):
				pos = self.enemies['right']['Bamboo'][index]
				Enemy(pos, [self.visible_sprites, self.enemy], 'Bamboo', self.obstacle_sprites, self.player, self.enemy_speed_index, dificulty)
				self.enemy_speed_index += 0.5
				index += 1

			index = 0
			for f in range(3):
				pos = self.enemies['right']['Reptile'][index]
				Enemy(pos, [self.visible_sprites, self.enemy], 'Reptile', self.obstacle_sprites, self.player, self.enemy_speed_index, dificulty)
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

	def walk_from_player_if_dead(self):
		if self.player.dead:
			for enemy in self.enemy:
				if enemy.hitbox.colliderect(self.player.rect.inflate(50,50)):
					enemy.direction.x *= (-1)			
					enemy.direction.y *= (-1)
						

	# PLAYER
	def damage_player(self,dificulty):
		if not self.player.dead:
			for enemy in self.enemy.sprites():
				if enemy.can_attack and self.player.vulnerable and enemy.direction == (0,0):
					self.player.health -= ENEMY_DAMAGE[dificulty][enemy.type]
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
		if self.clear_tm <= 50 and self.enemy_count == 0 and self.get_island() != 'start':
			self.clear_tm += 1
		if self.enemy_count != 0:
			self.clear_tm = 0

		if self.clear_tm == 1:
			self.t_clear_animate = True
			self.t_clear_index = 0

		if int(self.t_clear_index) == 2:
			self.t_clear_speed = 0.01
		else:
			self.t_clear_speed = 0.1
	


		if self.t_clear_animate:
			self.screen.blit(self.t_clear_image, self.t_clear_rect)
			if self.t_clear_index <= len(self.t_clear_frames):
				self.t_clear_image = self.t_clear_frames[int(self.t_clear_index)]
				self.t_clear_index += self.t_clear_speed
			else:
				self.t_clear_animate = False

	def death_text(self):
		if self.player.dead:
			self.screen.blit(self.death_text_img, self.death_text_rect)
			self.screen.blit(self.playagain_txt, self.playagain_rect)
			if self.death_text_index <= 2:
				self.playagain_alpha += 7
				self.playagain_txt.set_alpha(self.playagain_alpha)
				self.death_text_index += self.death_text_speed
				self.death_text_img = self.death_text_frames[int(self.death_text_index)]
			

			if int(self.death_text_index) >= 2:
				if self.player.want_restart:
					if self.death_text_index <= 4:
						self.playagain_alpha -= 10
						self.playagain_txt.set_alpha(self.playagain_alpha)
						self.death_text_index += self.death_text_speed
						self.death_text_img = self.death_text_frames[int(self.death_text_index)]
					else:
						self.death_text_img.set_alpha(0)

	def clear_island(self):
		if self.enemy_count == 0:
			self.clear = True

	# RUN
	def run(self,dificulty):
		self.visible_sprites.custom_draw(self.player)
		self.visible_sprites.update()
		self.input()
		self.clear_island()
		self.kill_enemy()
		self.damage_player(dificulty)
		self.baricade_animations()
		self.create_chests()
		self.trap_in_level(dificulty)
		self.draw_gui()
		self.clear_text()
		self.death_text()

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
