import pygame
from support import Sprite_sheet


class Enemy(pygame.sprite.Sprite):
	def __init__(self, pos, groups, type):
		super().__init__(groups)
		# sprite sheet
		path = 'graphics/monsters/' + type + '.png'
		sprite_sheet = Sprite_sheet(path)
		idle = sprite_sheet.get_image(0,0)

		# set up
		self.image = idle
		self.rect = self.image.get_rect(topleft=pos)

