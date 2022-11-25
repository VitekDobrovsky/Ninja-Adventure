import pygame
from settings import *
from support import Sprite_sheet
from random import randint


class Enemy(pygame.sprite.Sprite):
	def __init__(self, pos, groups, type, obstacle_sprites, player, speed):
		super().__init__(groups)
		# sprite sheet
		path = 'graphics/monsters/' + type + '.png'
		self.sprite_sheet = Sprite_sheet(path)
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

	def update(self):
		self.move()
		self.get_status()
		self.animate()

