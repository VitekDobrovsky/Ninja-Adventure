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
			

	def update(self):
		self.input()
		self.move()
