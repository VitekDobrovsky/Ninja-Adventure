import pygame
from support import Sprite_sheet
from settings import *


class Chest(pygame.sprite.Sprite):
	def __init__(self,pos,groups,player):
		super().__init__(groups)
		self.sheet = Sprite_sheet('graphics/tiles/BigTreasureChest.png')
		self.image = self.sheet.get_image(0,0)
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(-50, HITBOX_OFFSET_Y['chest'])
		self.opening_area = self.rect.inflate(200, 200)
		self.open_chest = self.sheet.get_image(0,1)
		self.player = player

	def open(self):
		if self.player.hitbox.colliderect(self.opening_area):
			self.image = self.open_chest

	def update(self):
		self.open()