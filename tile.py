import pygame
from settings import *
from support import import_folder
from support import Sprite_sheet
from random import choice


class Tile(pygame.sprite.Sprite):
	def __init__(self, pos, groups, type):
		super().__init__(groups)
		# main tile
		path = 'graphics/tiles/rock.png'
		self.image = pygame.image.load(path).convert_alpha()
		self.groups = groups

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

class Baricade(pygame.sprite.Sprite):
	def __init__(self, pos, groups, baricades, place):
		super().__init__(groups)
		# main tile
		self.sprite_sheet = Sprite_sheet('graphics/tiles/baricades/rocks_test.png', (16, 16), (64, 64)) 
		self.image = self.sprite_sheet.get_image(0,3)
		self.frames = [self.sprite_sheet.get_image(0,3), self.sprite_sheet.get_image(0,2), self.sprite_sheet.get_image(0,1), self.sprite_sheet.get_image(0,0)]
		self.groups = groups
		self.place = place
		self.baricades = baricades 

		# making hitbox
		self.rect = self.image.get_rect(topleft=pos)
		self.hitbox = self.rect

		self.baricades.append(self)
		self.clear_time = None
		self.help = True

	def add_frame(self, index):
		self.image = self.frames[index]

	def check(self, island, clear):
		if clear and self.help:
			self.clear_time = pygame.time.get_ticks()
			self.help = False

		if self.place == island:
			if clear and pygame.time.get_ticks() - self.clear_time >= 4500:
				self.baricades.remove(self)
				self.kill()