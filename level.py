import pygame
from settings import *
from tile import Tile
from tile import Baricade
from player import Player
from support import *
from enemy import Enemy
from random import randint
from math import sin 


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

		# enemy damage
		self.can_enemy_damage = True
		self.enemy_damage_time = None
		self.enemy_damage_cooldown = 500
		self.enemy_count = 0

		# 'CLEAR' text
		self.text1 = Text(self.screen, 'clear', 'graphics/fonts/Gameplay.ttf', 100, (WIDTH/2, HEIGHT/3), 'orange'), Text(self.screen, 'clear', 'graphics/fonts/Gameplay.ttf', 105, (WIDTH/2, HEIGHT/3), 'black')	
		self.text1[0].text_surf.set_alpha(0)
		self.text1[1].text_surf.set_alpha(0)
		self.al = 0
		self.clear_tm = 0

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

	def wave_value(self):
		# sin value
		value = sin(pygame.time.get_ticks())

		# choose
		if value > 0:
			return 225
		else:
			return 0

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

	def spawn_enemies(self):
		# current island
		current = self.get_island()

		# middle enemies
		if current == 'middle':
			for g in range(2):
				pos = self.enemies['middle']['Bamboo'][randint(0, 3)]
				Enemy(pos, [self.visible_sprites, self.enemy], 'Bamboo', self.obstacle_sprites, self.player, self.enemy_speed_index)
				self.enemy_speed_index += 0.5

			for l in range(2):
				pos = self.enemies['middle']['Racoon'][randint(0,3)]
				Enemy(pos, [self.visible_sprites, self.enemy], 'Racoon', self.obstacle_sprites, self.player, self.enemy_speed_index)
				self.enemy_speed_index += 0.5
				
			self.traped1 = False
			self.enemy_speed_index = 1

		# top enemies
		if current == 'top':
			for a in range(2):
				pos = self.enemies['top']['Racoon'][randint(0, 3)]
				Enemy(pos, [self.visible_sprites, self.enemy], 'Racoon', self.obstacle_sprites, self.player, self.enemy_speed_index)
				self.enemy_speed_index += 0.5

			for b in range(2):
				pos = self.enemies['top']['Spirit_fire'][randint(0,3)]
				Enemy(pos, [self.visible_sprites, self.enemy], 'Spirit_fire', self.obstacle_sprites, self.player, self.enemy_speed_index)
				self.enemy_speed_index += 0.5

			self.traped2 = False
			self.enemy_speed_index = 1

		# left enemies
		if current == 'left':
			for c in range(2):
				pos = self.enemies['left']['Racoon'][randint(0, 3)]
				Enemy(pos, [self.visible_sprites, self.enemy], 'Racoon', self.obstacle_sprites, self.player, self.enemy_speed_index)
				self.enemy_speed_index += 0.5
				self.enemy_speed_index = 1

			for d in range(2):
				pos = self.enemies['left']['Reptile'][randint(0,3)]
				Enemy(pos, [self.visible_sprites, self.enemy], 'Reptile', self.obstacle_sprites, self.player, self.enemy_speed_index)
				self.enemy_speed_index += 0.5

			self.traped3 = False
			self.enemy_speed_index = 1

		# right enemies
		if current == 'right':
			for e in range(2):
				pos = self.enemies['right']['Bamboo'][randint(0, 3)]
				Enemy(pos, [self.visible_sprites, self.enemy], 'Bamboo', self.obstacle_sprites, self.player, self.enemy_speed_index)
				self.enemy_speed_index += 0.5

			for f in range(2):
				pos = self.enemies['right']['Reptile'][randint(0,3)]
				Enemy(pos, [self.visible_sprites, self.enemy], 'Reptile', self.obstacle_sprites, self.player, self.enemy_speed_index)
				self.enemy_speed_index += 0.5

			self.traped4 = False
			self.enemy_speed_index = 1

	def enemy_move(self):
		for enemy in self.enemy.sprites():
			if self.player.hitbox.x + 64 < enemy.hitbox.x:
				enemy.direction.x = -1
			elif self.player.hitbox.x - 64 > enemy.hitbox.x:
				enemy.direction.x = 1
			else:
				enemy.direction.x = 0

			if self.player.hitbox.y + 64 < enemy.hitbox.y:
				enemy.direction.y = -1
			elif self.player.hitbox.y - 64 > enemy.hitbox.y:
				enemy.direction.y = 1
			else:
				enemy.direction.y = 0

	def trap_in_level(self):
		current = self.get_island()
		
		if current == 'middle' and not self.traped1:
			# middle baricades
			bar1 = Baricade(self.baricades['middle']['vertical'][0], [self.visible_sprites, self.obstacle_sprites], 'baricade_vertical', 'middle')
			bar2 = Baricade(self.baricades['middle']['vertical'][1], [self.visible_sprites, self.obstacle_sprites], 'baricade_vertical', 'middle')
			bar3 = Baricade(self.baricades['middle']['horizontal'][0], [self.visible_sprites, self.obstacle_sprites], 'baricade_horizontal', 'middle')
			bar4 = Baricade(self.baricades['middle']['horizontal'][1], [self.visible_sprites, self.obstacle_sprites], 'baricade_horizontal', 'middle')
			
			# append baricades to list
			self.baricades_sprites.append(bar1)
			self.baricades_sprites.append(bar2)
			self.baricades_sprites.append(bar3)
			self.baricades_sprites.append(bar4)
			
			# enemies set up for island
			self.spawn_enemies()
			self.count_enemies()

			self.traped1 = True
			self.clear = False

		elif current == 'top' and not self.traped2:
			# top baricades
			bar5 = Baricade(self.baricades['up'][0], [self.visible_sprites, self.obstacle_sprites], 'baricade_horizontal', 'top')
			
			self.baricades_sprites.append(bar5)
			
			# enemies set up for island
			self.spawn_enemies()
			self.count_enemies()

			self.traped2 = True
			self.clear = False

		elif current == 'left' and not self.traped3:
			# left baricades
			bar6 = Baricade(self.baricades['left'][0], [self.visible_sprites, self.obstacle_sprites], 'baricade_vertical', 'left')
			self.baricades_sprites.append(bar6)
			
			# enemies set up for island
			self.spawn_enemies()
			self.count_enemies()

			self.traped3 = True
			self.clear = False

		elif current == 'right' and not self.traped4:
			# right baricades
			bar7 = Baricade(self.baricades['right'][0], [self.visible_sprites, self.obstacle_sprites], 'baricade_vertical', 'right')
			self.baricades_sprites.append(bar7)
			
			# enemies set up for island
			self.spawn_enemies()
			self.count_enemies()

			self.traped4 = True
			self.clear = False


		# removing baricades
		for baricade in self.baricades_sprites:
			baricade.check(current, self.clear)

	def push_enemy(self, enemy):
		# knockback distance
		distance = 20

		if self.player.charge:
			# x
			if self.player.direction.x > 0:
				enemy.direction.x = distance
			elif self.player.direction.x < 0:
				enemy.direction.x = -distance

			# y
			if self.player.direction.y > 0:
				enemy.direction.y = distance
			elif self.player.direction.y < 0:
				enemy.direction.y = -distance

	def damage_enemy(self):
		for enemy in self.enemy.sprites():
			if self.player.weapon.rect.colliderect(enemy) and self.player.is_weapon:
				# push enemy
				self.push_enemy(enemy)
				
				# animation
				alpha = self.wave_value()
				enemy.image.set_alpha(alpha)

				if self.can_enemy_damage:
					# cooldown
					self.enemy_damage_time = pygame.time.get_ticks()
					self.can_enemy_damage = False

					# subtract health
					enemy.health -= self.player.weapon.damage
					if enemy.health <= 0:
						enemy.kill()
						self.enemy_count -= 1
			else:
				enemy.image.set_alpha(255)

	def count_enemies(self):
		for enemy in self.enemy.sprites():
			self.enemy_count += 1

	def clear_text(self):
		if self.al >= 0:
			self.al -= 5
		self.text1[1].draw()
		self.text1[0].draw()
		self.text1[0].text_surf.set_alpha(self.al)
		self.text1[1].text_surf.set_alpha(self.al)

		if self.clear_tm <= 50 and self.enemy_count == 0 and self.get_island() != 'start':
			self.clear_tm += 1
			#self.text1.text_surf.set_alpha(255)
			self.al = 255
		if self.enemy_count != 0:
			self.clear_tm = 0

	def clear_island(self):
		if self.enemy_count == 0:
			self.clear = True

	def cooldown(self):
		current_time = pygame.time.get_ticks()

		if not self.can_enemy_damage:
			if current_time - self.enemy_damage_time >= self.enemy_damage_cooldown:
				self.can_enemy_damage = True

	def run(self):
		self.visible_sprites.custom_draw(self.player)
		self.visible_sprites.update()
		self.clear_island()
		self.enemy_move()
		self.damage_enemy()
		self.trap_in_level()
		self.clear_text()
		self.cooldown()

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
