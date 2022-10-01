import pygame
from settings import *


class Player(pygame.sprite.Sprite):
	def __init__(self, pos, groups, obstacle_sprites):
		super().__init__(groups)
		# set up
		self.image = pygame.image.load('graphics/player/down/down_0.png')
		self.rect = self.image.get_rect(topleft=pos)

		# move
		self.direction = pygame.math.Vector2()
		self.speed = player_stats['speed']

		# colision
		self.obstacle_sprites = obstacle_sprites

		# animation
		self.status = 'down'

	def input(self):
		keys = pygame.key.get_pressed()

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

	def move(self):
		if self.direction.magnitude() != 0:
			self.direction.normalize()

		self.rect.x += self.direction.x * self.speed
		self.colision('horizontal')
		self.rect.y += self.direction.y * self.speed
		self.colision('vertical')

	def colision(self, direction):
		if direction == 'horizontal':
			for sprite in self.obstacle_sprites:
				if sprite.rect.colliderect(self.rect):
					if self.direction.x > 0:
						self.rect.right = sprite.rect.left
					if self.direction.x < 0:
						self.rect.left = sprite.rect.right
		elif direction == 'vertical':
			for sprite in self.obstacle_sprites:
				if sprite.rect.colliderect(self.rect):
					if self.direction.y > 0:
						self.rect.bottom = sprite.rect.top
					if self.direction.y < 0:
						self.rect.top = sprite.rect.bottom
		
	def get_status(self):
		if self.direction.y < 0:
			self.status = 'up'
		elif self.direction.y > 0:
			self.status = 'down'
		else:
			if len(self.status) < 6:
				if self.direction.x == 0:
					self.status += '_idle'
		if self.direction.x > 0:
			self.status = 'right'
		elif self.direction.x < 0:
			self.status = 'left'
		else:
			if len(self.status) < 6:
				if self.direction.y == 0:
					self.status += '_idle'

	def update(self):
		self.input()
		self.move()
		self.get_status()
		print(self.status)
