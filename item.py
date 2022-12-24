import pygame
from random import randint


class Item(pygame.sprite.Sprite):
	def __init__(self, pos, list, visible_sprites):
		super().__init__()

		self.list = list
		self.index = 0
		self.animation_speed = 0.15

		self.image = self.list[self.index]
		self.rect = self.image.get_rect(center=pos)
		self.def_pos = pos

		# chest animation
		self.direction = pygame.math.Vector2()
		self.speed = 2
		self.up = True
		self.height = -15
		self.up_index = 1
		self.visible_sprites = visible_sprites
		self.at_floor = False
		self.added = False
		self.picked = False

	def items_from_chest(self, player, x_side):
		current_time = pygame.time.get_ticks()
		if not self.added:
			self.visible_sprites.add(self)
			self.added = True

		if self.up_index <= 10:
			# x
			self.direction.x = x_side
			# y
			self.direction.y = -1
			
			# increase index
			self.up_index += 1
			self.speed -= 0.22

		else:
			self.up = False
			self.direction.y = 0
			self.direction.x = 0

		if not self.up:
			self.direction.y = 1
			random = randint(0 ,50)
			if self.rect.y >= self.def_pos[1] - random and not self.at_floor:
				self.direction.y = 0
				self.at_floor = True

			if self.at_floor:
				self.direction.y = 0

			if player.hitbox.colliderect(self.rect) and self.at_floor:
				self.picked = True
				self.kill()

		self.rect.x += self.direction.x * (self.speed + 5)
		self.rect.y += self.direction.y * self.speed