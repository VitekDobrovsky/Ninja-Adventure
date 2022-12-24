import pygame
from settings import *
from support import *
from weapon import Weapon
from particles import Particle


class Player(pygame.sprite.Sprite):
	def __init__(self, pos, groups, obstacle_sprites, visible_sprites):
		super().__init__(groups)
		
		# sprite sheets
		self.idle_sheet = Sprite_sheet('graphics/player/Idle.png', (16, 16), (64, 64))
		self.walk_sheet = Sprite_sheet('graphics/player/Walk.png', (16, 16), (64, 64))
		self.attack_sheet = Sprite_sheet('graphics/player/Attack.png', (16, 16), (64, 64))

		# animation frames
		self.frames = {
			'down_idle': [self.idle_sheet.get_image(0,0), self.idle_sheet.get_image(0,0), self.idle_sheet.get_image(0,0), self.idle_sheet.get_image(1,0), self.idle_sheet.get_image(1,0), self.idle_sheet.get_image(1,0), self.idle_sheet.get_image(1,0)],
			'up_idle': [self.idle_sheet.get_image(0,1), self.idle_sheet.get_image(0,1), self.idle_sheet.get_image(0,1), self.idle_sheet.get_image(1,1), self.idle_sheet.get_image(1,1), self.idle_sheet.get_image(1,1), self.idle_sheet.get_image(1,1)],
			'left_idle': [self.idle_sheet.get_image(0,2), self.idle_sheet.get_image(0,2), self.idle_sheet.get_image(0,2), self.idle_sheet.get_image(1,2), self.idle_sheet.get_image(1,2), self.idle_sheet.get_image(1,2), self.idle_sheet.get_image(1,2)],
			'right_idle': [self.idle_sheet.get_image(0,3), self.idle_sheet.get_image(0,3), self.idle_sheet.get_image(0,3), self.idle_sheet.get_image(1,3), self.idle_sheet.get_image(1,3), self.idle_sheet.get_image(1,3), self.idle_sheet.get_image(1,3)],
			'down': [self.walk_sheet.get_image(0,0), self.walk_sheet.get_image(1,0),
					self.walk_sheet.get_image(2,0), self.walk_sheet.get_image(3,0)],
			'up': [self.walk_sheet.get_image(0,1), self.walk_sheet.get_image(1,1),
					self.walk_sheet.get_image(2,1), self.walk_sheet.get_image(3,1)],
			'left': [self.walk_sheet.get_image(0,2), self.walk_sheet.get_image(1,2),
					self.walk_sheet.get_image(2,2), self.walk_sheet.get_image(3,2)],
			'right': [self.walk_sheet.get_image(0,3), self.walk_sheet.get_image(1,3),
					self.walk_sheet.get_image(2,3), self.walk_sheet.get_image(3,3)],
			'down_attack': [self.attack_sheet.get_image(0,0)],
			'up_attack': [self.attack_sheet.get_image(0,1)],
			'left_attack': [self.attack_sheet.get_image(0,2)],
			'right_attack': [self.attack_sheet.get_image(0,3)]
			}

		# player set up
		self.image = self.frames['down_idle'][0]
		self.rect = self.image.get_rect(topleft=pos)
		self.hitbox = self.rect.inflate(-6, HITBOX_OFFSET_Y['player'])
		self.screen = pygame.display.get_surface()

		# move
		self.direction = pygame.math.Vector2()
		self.speed = player_stats['speed']

		# groups
		self.obstacle_sprites = obstacle_sprites
		self.visible_sprites = visible_sprites

		# animation
		self.status = 'down_idle'
		self.frame_index = 0
		self.frame_speed = 0.17

		# heal animation
		self.heal_sheet = Sprite_sheet('graphics/player/Heal.png', (32, 32), (128, 128))
		self.heal_particle = Particle(self, self.heal_sheet, self.visible_sprites, 3, 'health')
		self.heal_animation = False

		# energy boost animation
		self.energy_boost_sheet = Sprite_sheet('graphics/player/Boost_energy.png', (32, 32), (128, 128))
		self.energy_boost_particle = Particle(self, self.energy_boost_sheet, self.visible_sprites, 3, 'energy')
		self.energy_boost_animation = False

		# stats
		self.health = player_stats['health']
		self.energy = player_stats['energy']

		# take_damage
		self.vulnerable = True 
		self.damage_time = None
		self.damage_cooldown = 400

		# attack
		self.can_attack = True
		self.attack_cooldown = 600
		self.attack_time = None
		self.attack = False

		# weapon
		self.sword = Weapon(self.rect, self.status, self.visible_sprites, 'sword')
		self.lance = Weapon(self.rect, self.status, self.visible_sprites, 'lance')
		self.weapon = [self.sword, self.lance]
		self.weapon_index = 0
		self.can_change_weapon = True
		self.change_weapon_cooldown = 200
		self.change_weapon_time = None
		self.is_weapon = False

		# charge
		self.charge = False
		self.charge_cooldown = 100
		self.charge_time = None

		# stop after attack
		self.stop = False 
		self.stop_cooldown = 200
		self.stop_time = None 

	def input(self):
		keys = pygame.key.get_pressed()

		# evet handler
		if keys[pygame.K_w]:
			self.direction.y = -1
		elif keys[pygame.K_s]:
			self.direction.y = 1
		else:
			self.direction.y = 0

		if keys[pygame.K_d]:
			self.direction.x = 1
		elif keys[pygame.K_a]:
			self.direction.x = -1
		else:
			self.direction.x = 0

		if keys[pygame.K_SPACE] and self.can_attack and self.energy >= 5:
			# attack cooldown
			self.attack = True
			self.attack_time = pygame.time.get_ticks()
			self.can_attack = False

		# subtract player energy
			if self.energy > 1:
				self.energy -= 5
			else:
				self.energy = 0

			# charge cooldown
			self.charge = True
			self.charge_time = pygame.time.get_ticks()

			# stop after charge
			self.stop = True 
			self.stop_time = pygame.time.get_ticks()

		if keys[pygame.K_r] and self.can_change_weapon:
			if self.weapon_index < 1:
				self.weapon_index += 1
			else:
				self.weapon_index = 0

			self.change_weapon_time = pygame.time.get_ticks()
			self.can_change_weapon = False

	def move(self):
		# normalize direction
		if self.direction.magnitude() != 0:
			self.direction.normalize()

		# charge
		distance = 2.5
		if self.charge:
			if self.status == 'down_attack':
				self.direction.y = distance
			elif self.status == 'up_attack':
				self.direction.y = -distance
			elif self.status == 'right_attack':
				self.direction.x = distance
			elif self.status == 'left_attack':
				self.direction.x = -distance

		# stop after charge
		if self.stop and not self.charge:
			self.direction.y = 0
			self.direction.x = 0

		# apply move
		self.hitbox.x += self.direction.x * self.speed
		self.colision('horizontal')
		self.hitbox.y += self.direction.y * self.speed
		self.colision('vertical')

		# matching hitbox
		self.rect.center = self.hitbox.center

	def colision(self, direction):
		# check horiziontal collision
		if direction == 'horizontal':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.x > 0:
						self.hitbox.right = sprite.hitbox.left
					if self.direction.x < 0:
						self.hitbox.left = sprite.hitbox.right

		# check vertical collision
		elif direction == 'vertical':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.y > 0:
						self.hitbox.bottom = sprite.hitbox.top
					if self.direction.y < 0:
						self.hitbox.top = sprite.hitbox.bottom
	
	def normalize_health(self):
		if self.health > player_stats['health']:
			self.health = player_stats['health']

	def normalize_energy(self):
		if self.energy > player_stats['energy']:
			self.energy = player_stats['energy']

	def get_status(self):
		# getting y status
		if self.direction.y < 0:
			self.status = 'up'
		elif self.direction.y > 0:
			self.status = 'down'
		else:
			if len(self.status) < 6:
				if self.direction.x == 0:
					self.status += '_idle'
		
		# getting x status
		if self.direction.x > 0:
			self.status = 'right'
		elif self.direction.x < 0:
			self.status = 'left'
		else:
			if len(self.status) < 6:
				if self.direction.y == 0:
					self.status += '_idle'
		
		# adding attack to status
		if self.charge or self.stop:
			self.status = self.status.replace('_idle', '')
			if len(self.status) < 6:
				self.status += '_attack'
		else:
			self.status = self.status.replace('_attack', '')

	def animate(self):
		# animation
		animation = self.frames[self.status]
		self.frame_index += self.frame_speed

		if self.frame_index >= len(animation):
			self.frame_index = 0

		self.image = animation[int(self.frame_index)]

		# heal animation
		if self.heal_animation:
			self.heal_particle.one_time_animation()

		if self.energy_boost_animation:
			self.energy_boost_particle.one_time_animation()


	def draw_weapon(self):
		# draw weapon
		if self.charge or self.stop:
			self.weapon[self.weapon_index].status = self.status
			self.weapon[self.weapon_index].player_rect = self.rect
			self.weapon[self.weapon_index].show()
			self.is_weapon = True
		else:
			self.weapon[self.weapon_index].kill()
			self.is_weapon = False

	def add_energy(self):
		if self.energy < player_stats['energy']:
			self.energy += 0.02

	def cooldown(self):
		current_time = pygame.time.get_ticks()

		# attack cooldown
		if not self.can_attack:
			if current_time - self.attack_time >= self.attack_cooldown:
				self.can_attack = True
				self.attack = False

		# charge cooldown
		if self.charge:
			if current_time - self.charge_time >= self.charge_cooldown:
				self.charge = False

		# timing stop
		if self.stop:
			if current_time - self.stop_time >= self.stop_cooldown:
				self.stop = False

		# vulnerable cooldown
		if not self.vulnerable:
			if current_time - self.damage_time >= self.damage_cooldown:
				self.vulnerable = True

		# change weapon cooldown
		if not self.can_change_weapon:
			if current_time - self.change_weapon_time >= self.change_weapon_cooldown:
				self.can_change_weapon = True

	def update(self):
		self.cooldown()
		self.input()
		self.add_energy()
		self.move()
		self.get_status()
		#self.normalize_health()
		#self.normalize_energy()
		self.draw_weapon()
		self.animate()
		