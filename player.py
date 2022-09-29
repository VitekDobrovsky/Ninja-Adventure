import pygame
from settings import *


class Player(pygame.sprite.Sprite):
	def __init__(self, pos, groups):
		super().__init__(groups)
		# set up
		self.image = pygame.image.load('graphics/player/down_0.png')
		self.rect = self.image.get_rect(topleft=pos)

		# move
		self.direction = pygame.math.Vector2()
		self.speed = player_stats['speed']

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
		self.rect.y += self.direction.y * self.speed

	def update(self):
		self.input()
		self.move()
