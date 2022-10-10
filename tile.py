import pygame
from settings import *
from support import import_folder
from random import choice


class Tile(pygame.sprite.Sprite):
	def __init__(self, pos, groups, type):
		super().__init__(groups)
		path = 'graphics/test/rock.png'
		self.image = pygame.image.load(path).convert_alpha()
		if type == 'grass':
			self.image = choice(import_folder('graphics/tiles/grass'))
			
		self.rect = self.image.get_rect(topleft=pos)
		self.hitbox = self.rect.inflate(-30, HITBOX_OFFSET[type])