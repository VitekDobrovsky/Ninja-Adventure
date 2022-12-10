import pygame
from support import Sprite_sheet


class ParticleEffect(pygame.sprite.Sprite):
	def __init__(self, pos, list, visible_sprites):
		super().__init__()

		self.list = list
		self.index = 0
		self.animation_speed = 0.15

		self.image = self.list[self.index]
		self.rect = self.image.get_rect(center=pos)

		# go to player animation
		self.direction = pygame.math.Vector2()
		self.speed = 5
		self.up = True
		self.height = pygame.math.Vector2(0, -15)
		self.up_index = 1
		self.visible_sprites = visible_sprites

	def short_animate(self):
		if self.index > len(self.list):
			self.kill()
		else:
			self.index += self.animation_speed
			self.image = self.list[float(self.index)]

	def go_to_player_animation(self, player):
		current_time = pygame.time.get_ticks()
		self.visible_sprites.add(self)

		if self.up_index <= 10:
			self.up_index += 1
			self.rect.y += self.height.y
		else:
			self.up = False

		if not self.up:
			if player.hitbox.centerx < self.rect.centerx:
				self.direction.x = -1
			elif player.hitbox.centerx > self.rect.centerx:
				self.direction.x = 1
			else:
				self.direction.y = 0

			if player.hitbox.centery < self.rect.centery:
				self.direction.y = -1
			elif player.hitbox.centery > self.rect.centery:
				self.direction.y = 1
			else:
				self.direction.y = 0

			if player.hitbox.colliderect(self.rect):
				self.kill()

		self.rect.x += self.direction.x * self.speed
		self.rect.y += self.direction.y * self.speed