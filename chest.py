import pygame
from support import Sprite_sheet
from particles import ParticleEffect
from settings import *


class Chest(pygame.sprite.Sprite):
	def __init__(self,pos,groups,player,screen, visible_sprites):
		super().__init__(groups)
		self.sheet = Sprite_sheet('graphics/tiles/BigTreasureChest.png')
		self.image = self.sheet.get_image(0,0)
		self.open_chest = self.sheet.get_image(0,1)

		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(-30, HITBOX_OFFSET_Y['chest'])
		self.opening_area = self.rect.inflate(50, 50)
		
		self.player = player
		self.screen = screen
		self.visible_sprites = visible_sprites

		self.is_open = False
		self.open_index = 0

		self.health_amout = 20
		self.energy_amount = 20

		# energy
		self.energy_image = pygame.image.load('graphics/GUI/energy.png').convert_alpha()
		self.energy_image = pygame.transform.scale(self.energy_image, (BAR_HEIGHT + 7, BAR_HEIGHT + 7))
		self.energy_image.set_colorkey((20, 27, 27))
		self.energy = ParticleEffect(self.rect.center, [self.energy_image], self.visible_sprites)

		# heart
		self.heart_image = pygame.image.load('graphics/GUI/heart.png').convert_alpha()
		self.heart_image = pygame.transform.scale(self.heart_image, (BAR_HEIGHT + 8, BAR_HEIGHT + 8))
		self.heart_image.set_colorkey((20, 27, 27))
		self.heart = ParticleEffect(self.rect.center, [self.heart_image], self.visible_sprites)

		# animate
		self.open_time = None

	def open(self):
		if self.player.hitbox.colliderect(self.opening_area):
			self.image = self.open_chest
			if self.open_index == 0:
				self.open_time = pygame.time.get_ticks()
				self.is_open = True

	def blit_items(self):
		if self.open_index == 1:
			current_time = pygame.time.get_ticks()
			if current_time - self.open_time >= 250:
				self.heart.go_to_player_animation(self.player)
			
			self.energy.go_to_player_animation(self.player)

	def give_content(self):
		if self.is_open:
			# give stats
			# TODO: animation
			if self.player.health <= 80:
				self.player.health += 20
			else:
				self.player.health += player_stats['health'] - self.player.health
			
			if self.player.energy <= 80:
				self.player.energy += 20
			else:
				self.player.energy += player_stats['energy'] - self.player.energy
			
			self.is_open = False
			self.open_index = 1

	def update(self):
		self.blit_items()
		self.open()
		self.give_content()