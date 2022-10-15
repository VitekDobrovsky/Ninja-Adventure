import pygame
from settings import *
from support import *
from weapon import Weapon


class Player(pygame.sprite.Sprite):
	def __init__(self, pos, groups, obstacle_sprites, visible_sprites):
		super().__init__(groups)
		# sprite sheets set up
		self.idle_sheet = Sprite_sheet('graphics/player/Idle.png')
		self.walk_sheet = Sprite_sheet('graphics/player/Walk.png')
		self.attack_sheet = Sprite_sheet('graphics/player/Attack.png')

		# frames
		self.frames = {
			'down_idle': [self.idle_sheet.get_image(0,0)],
			'up_idle': [self.idle_sheet.get_image(0,1)],
			'left_idle': [self.idle_sheet.get_image(0,2)],
			'right_idle': [self.idle_sheet.get_image(0,3)],
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

		# set up
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
		self.frame_speed = 0.15

		# bars
		self.health = player_stats['health']
		self.energy = player_stats['energy']

		# attack
		self.can_attack = True
		self.attack_cooldown = 600
		self.attack_time = None
		self.attack = False

		# weapon
		self.weapon = Weapon(self.rect, self.status, self.visible_sprites)

		# charge
		self.charge = False
		self.charge_cooldown = 150
		self.charge_time = None

		# stop after attacl
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

		if keys[pygame.K_SPACE] and self.can_attack:
			# time
			self.attack = True
			self.attack_time = pygame.time.get_ticks()
			self.can_attack = False

			# charge
			self.charge = True
			self.charge_time = pygame.time.get_ticks()

			# stop after charge
			self.stop = True 
			self.stop_time = pygame.time.get_ticks()

	def move(self):
		# normalize direction
		if self.direction.magnitude() != 0:
			self.direction.normalize()

		# push forward while attack
		distance = 3
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
				
		if self.charge:
			self.status = self.status.replace('_idle', '')
			if len(self.status) < 6:
				self.status += '_attack'
		else:
			self.status = self.status.replace('_attack', '')

	def animate(self):
		animation = self.frames[self.status]

		self.frame_index += self.frame_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		self.image = animation[int(self.frame_index)]

	def health_bar(self):
		# draw health bar
		draw_rect(self.screen,10,10, 200, BAR_HEIGHT, (134,122,4))
		draw_rect(self.screen,10,10, self.health, BAR_HEIGHT, (255,0,0))
		overlay = pygame.image.load('graphics/GUI/health_bar.png')
		overlay_rect = overlay.get_rect(topleft= (5,5))
		self.screen.blit(overlay, overlay_rect)
		
		# draw energy bar
		draw_rect(self.screen,9,36, 152, BAR_HEIGHT, (114,106,133))
		draw_rect(self.screen,10,36, self.energy, BAR_HEIGHT, (0,0,225))
		overlay_e = pygame.image.load('graphics/GUI/energy_bar.png')
		overlay_e_rect = overlay_e.get_rect(topleft= (5,31))
		self.screen.blit(overlay_e, overlay_e_rect)

	def show_weapon(self):
		if self.charge:
			#self.weapon = Weapon(self.rect, self.status, self.visible_sprites)
			self.weapon.status = self.status
			self.weapon.player_rect = self.rect
			self.weapon.show()
		else:
			self.weapon.remove()

	def cooldown(self):
		current_time = pygame.time.get_ticks()

		if not self.can_attack:
			if current_time - self.attack_time >= self.attack_cooldown:
				self.can_attack = True
				self.attack = False

		if self.charge:
			if current_time - self.charge_time >= self.charge_cooldown:
				self.charge = False

		if self.stop:
			if current_time - self.stop_time >= self.stop_cooldown:
				self.stop = False

	def update(self):
		self.cooldown()
		self.input()
		self.move()
		self.get_status()
		self.show_weapon()
		self.animate()
		self.health_bar()