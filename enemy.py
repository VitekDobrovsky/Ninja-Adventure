import pygame
from settings import *
from support import Sprite_sheet
from random import randint


class Enemy(pygame.sprite.Sprite):
	def __init__(self, pos, groups, type, obstacle_sprites, player, speed):
		super().__init__(groups)
		# sprite sheet
		path = 'graphics/monsters/' + type + '.png'
		self.sprite_sheet = Sprite_sheet(path, (16, 16), (64, 64))
		idle = self.sprite_sheet.get_image(0,0)

		# set up
		self.image = idle
		self.rect = self.image.get_rect(topleft=pos)
		self.hitbox = self.rect.inflate(-6, HITBOX_OFFSET_Y['enemy'])
		self.type = type

		# groups
		self.obstacle_sprites = obstacle_sprites
		self.player = player

		# move
		self.direction = pygame.math.Vector2()
		self.speed = speed
		self.last_direction = {
			'x': 0,
			'y': 0
			}
		self.collide = False

		# get damage
		self.can_enemy_damage = True
		self.enemy_damage_time = None
		self.enemy_damage_cooldown = 500

		# animate
		self.status = 'idle'
		self.frame_index = 0
		self.frame_speed = 0.17
		self.frames = {
			'down': [self.sprite_sheet.get_image(0,0), self.sprite_sheet.get_image(1,0),
					self.sprite_sheet.get_image(2,0), self.sprite_sheet.get_image(3,0)],
			'up': [self.sprite_sheet.get_image(0,1), self.sprite_sheet.get_image(1,1),
					self.sprite_sheet.get_image(2,1), self.sprite_sheet.get_image(3,1)],
			'left': [self.sprite_sheet.get_image(0,2), self.sprite_sheet.get_image(1,2),
					self.sprite_sheet.get_image(2,2), self.sprite_sheet.get_image(3,2)],
			'right': [self.sprite_sheet.get_image(0,3), self.sprite_sheet.get_image(1,3),
					self.sprite_sheet.get_image(2,3), self.sprite_sheet.get_image(3,3)],
			'idle': [self.sprite_sheet.get_image(0,0)]
			}

		# stats
		self.health = ENEMY_HEALTH[type]

		# attack
		self.can_attack = False


	def move(self):
		# normalize direction
		if self.direction.magnitude() != 0:
			self.direction.normalize()

		# apply move
		self.hitbox.x += self.direction.x * self.speed
		self.colision('horizontal')
		self.hitbox.y += self.direction.y * self.speed
		self.colision('vertical')

		# matching hitbox
		self.rect.center = self.hitbox.center

	def set_direction(self):
		if self.player.hitbox.x + 64 < self.hitbox.x:
			self.direction.x = -1
			self.can_attack = False
			self.last_direction['x'] = -1
		elif self.player.hitbox.x - 64 > self.hitbox.x:
			self.direction.x = 1
			self.can_attack = False
			self.last_direction['x'] = 1
		else:
			self.direction.x = 0
			self.can_attack = True
		
		if self.player.hitbox.y + 64 < self.hitbox.y:
			self.direction.y = -1
			self.can_attack = False
			self.last_direction['y'] = -1
		elif self.player.hitbox.y - 64 > self.hitbox.y:
			self.direction.y = 1
			self.can_attack = False
			self.last_direction['y'] = 1
		else:
			self.direction.y = 0
			self.can_attack = True

		if self.player.dead:
			if not self.collide:
				self.direction.x = self.last_direction['x'] * (-1)
				self.direction.y = self.last_direction['y'] * (-1)
			else:
				self.direction.x = 0
				self.direction.y = 0
			
				
	def get_status(self):
		# getting y status
		if self.direction.y < 0:
			self.status = 'up'
		elif self.direction.y > 0:
			self.status = 'down'
				
		# getting x status
		elif self.direction.x > 0:
			self.status = 'right'
		elif self.direction.x < 0:
			self.status = 'left'
		else:
			self.status = 'idle'

	def animate(self):
		# animation
		animation = self.frames[self.status]
		self.frame_index += self.frame_speed

		if self.frame_index >= len(animation):
			self.frame_index = 0

		self.image = animation[int(self.frame_index)]

	def colision(self, direction):
		# check horiziontal collision
		if direction == 'horizontal':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					self.collide = True
					if self.direction.x > 0:
						self.hitbox.right = sprite.hitbox.left
					if self.direction.x < 0:
						self.hitbox.left = sprite.hitbox.right

		# check vertical collision
		elif direction == 'vertical':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					self.collide = True
					if self.direction.y > 0:
						self.hitbox.bottom = sprite.hitbox.top
					if self.direction.y < 0:
						self.hitbox.top = sprite.hitbox.bottom

	def get_damage(self):
		if self.player.weapon[self.player.weapon_index].rect.colliderect(self) and self.player.is_weapon:
			# push enemy
			distance = 30
			if self.player.charge:
				# x
				if self.player.direction.x > 0:
					self.direction.x = distance
				elif self.player.direction.x < 0:
					self.direction.x = -distance

				# y
				if self.player.direction.y > 0:
					self.direction.y = distance
				elif self.player.direction.y < 0:
					self.direction.y = -distance

			if self.can_enemy_damage:
					# cooldown
					self.enemy_damage_time = pygame.time.get_ticks()
					self.can_enemy_damage = False

					# subtract health
					self.health -= self.player.weapon[self.player.weapon_index].damage

	def cooldown(self):
		current_time = pygame.time.get_ticks()

		if not self.can_enemy_damage:
			if current_time - self.enemy_damage_time >= self.enemy_damage_cooldown:
				self.can_enemy_damage = True

	def update(self):
		self.move()
		self.set_direction()
		self.get_damage()
		self.get_status()
		self.animate()
		self.cooldown()

class Dead_enemy(pygame.sprite.Sprite):
	def __init__(self, pos, groups, type):
		super().__init__(groups)
		path = 'graphics/monsters/dead/' + type + '.png'
		self.image = pygame.transform.scale(pygame.image.load(path).convert_alpha(), (64, 64))
		self.rect = self.image.get_rect(topleft=pos)
