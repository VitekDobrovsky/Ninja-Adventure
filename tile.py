import pygame
from settings import *
from support import import_folder
from random import choice


class Tile(pygame.sprite.Sprite):
	def __init__(self, pos, groups, type):
		super().__init__(groups)
		# main tile
		path = 'graphics/tiles/rock.png'
		self.image = pygame.image.load(path).convert_alpha()

		# diferent tiles
		if type == 'grass':
			self.image = choice(import_folder('graphics/tiles/grass')).convert_alpha()
		elif type == 'stubbe':
			self.image = choice(import_folder('graphics/tiles/logs')).convert_alpha()
		elif type == 'tree':
			self.image = choice(import_folder('graphics/tiles/trees')).convert_alpha()
		
		# custom rect on 2-block tiles
		self.rect = self.image.get_rect(topleft=pos)
		if type == 'tree' or type == 'stubbe':
			self.rect = self.image.get_rect(midleft=pos)

		# making hitbox
		self.hitbox = self.rect.inflate(HITBOX_OFFSET_X[type], HITBOX_OFFSET_Y[type])



