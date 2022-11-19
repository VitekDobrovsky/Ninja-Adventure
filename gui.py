import pygame
from support import draw_rect
from settings import *


class GUI:
	def __init__(self, player):
		self.screen = pygame.display.get_surface()
		self.player = player

	def health_bar(self):
		# draw health bar
		draw_rect(self.screen,10,10, 300, BAR_HEIGHT, (133, 106, 106), 255)
		draw_rect(self.screen,10,10, self.player.health, BAR_HEIGHT, (255,0,0), 255)
		
	def energy_bar(self):
		# draw energy bar
		draw_rect(self.screen,9,36, 150, BAR_HEIGHT, (114,106,133), 255)
		draw_rect(self.screen,10,36, self.player.energy, BAR_HEIGHT, (0,0,225), 255)

	def draw(self):
		self.health_bar()
		self.energy_bar()
