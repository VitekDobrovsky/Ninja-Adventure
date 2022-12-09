import pygame
from support import Sprite_sheet
from settings import *


class Chest(pygame.sprite.Sprite):
	def __init__(self,pos,groups,player):
		super().__init__(groups)
		self.sheet = Sprite_sheet('graphics/tiles/BigTreasureChest.png')
		self.image = self.sheet.get_image(0,0)
		self.open_chest = self.sheet.get_image(0,1)

		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(-30, HITBOX_OFFSET_Y['chest'])
		self.opening_area = self.rect.inflate(50, 50)
		
		self.player = player

		self.is_open = False
		self.open_index = 0

		self.health_amout = 20
		self.energy_amount = 20

	def open(self):
		if self.player.hitbox.colliderect(self.opening_area):
			self.image = self.open_chest
			if self.open_index == 0:
				self.is_open = True

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
		self.open()
		self.give_content()