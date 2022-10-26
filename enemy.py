import pygame
from settings import *
from support import Sprite_sheet
from random import randint


class Enemy(pygame.sprite.Sprite):
	def __init__(self, pos, groups, type, obstacle_sprites, player, speed):
		super().__init__(groups)
		# sprite sheet
		path = 'graphics/monsters/' + type + '.png'
		sprite_sheet = Sprite_sheet(path)
		idle = sprite_sheet.get_image(0,0)

		# set up
		self.image = idle
		self.rect = self.image.get_rect(topleft=pos)
		self.hitbox = self.rect.inflate(-6, HITBOX_OFFSET_Y['enemy'])

		# groups
		self.obstacle_sprites = obstacle_sprites
		self.player = player

		# move
		self.direction = pygame.math.Vector2()
		self.speed =  speed# TODO: diferent enemy = diferent speed, and get it from settings

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

	def colision(self, direction):
		# check horiziontal collision
		if direction == 'horizontal':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.x > 0:
						self.hitbox.right = sprite.hitbox.left
					if self.direction.x < 0:
						self.hitbox.left = sprite.hitbox.right
			if self.player.hitbox.colliderect(self.hitbox):
					if self.direction.x > 0:
						self.hitbox.right = self.player.hitbox.left
					if self.direction.x < 0:
						self.hitbox.left = self.player.hitbox.right

		# check vertical collision
		elif direction == 'vertical':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.y > 0:
						self.hitbox.bottom = sprite.hitbox.top
					if self.direction.y < 0:
						self.hitbox.top = sprite.hitbox.bottom
			if self.player.hitbox.colliderect(self.hitbox):
					if self.direction.y > 0:
						self.hitbox.bottom = self.player.hitbox.top
					if self.direction.y < 0:
						self.hitbox.top = self.player.hitbox.bottom

	def update(self):
		self.move()
		print(self.hitbox)

