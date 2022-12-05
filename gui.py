import pygame
from support import draw_rect
from settings import *


class GUI:
	def __init__(self, player):
		self.screen = pygame.display.get_surface()
		self.player = player

		# player faceset
		self.faceset_image = pygame.image.load('graphics/GUI/face_set.png').convert_alpha()
		self.faceset_image = pygame.transform.scale(self.faceset_image, (153 * 0.7, 143 * 0.7))
		self.faceset_rect = self.faceset_image.get_rect(center= (60,60))

		# golden ring
		self.ring_image = pygame.image.load('graphics/GUI/gold_circle.png').convert_alpha()
		self.ring_image = pygame.transform.scale(self.ring_image, (156 * 0.71, 157 * 0.71))
		self.ring_rect = self.ring_image.get_rect(center= (60,60))

		# map
		self.map_image = pygame.image.load('graphics/GUI/map.png').convert_alpha()
		self.map_image = pygame.transform.scale(self.map_image, (WIDTH * 0.5, WIDTH * 0.5))
		self.map_rect = self.map_image.get_rect(center= (WIDTH * 0.5 , HEIGHT * 0.5))

		# frame
		self.frame_image = pygame.image.load('graphics/GUI/frame.png').convert_alpha()
		self.frame_image = pygame.transform.scale(self.frame_image, (WIDTH * 0.5 + 50, WIDTH * 0.5 + 40))
		self.frame_rect = self.frame_image.get_rect(center= (WIDTH * 0.5 , HEIGHT * 0.5 ))

	def health_bar(self):
		# draw health bar
		draw_rect(self.screen,7,7, 306, BAR_HEIGHT + 6, '#FDD503')
		draw_rect(self.screen,10,10, 300, BAR_HEIGHT, (133, 106, 106))
		draw_rect(self.screen,10,10, self.player.health, BAR_HEIGHT, (255,0,0))
		
	def energy_bar(self):
		# draw energy bar
		draw_rect(self.screen,7,37, 156, BAR_HEIGHT + 6, '#C0C0C0')
		draw_rect(self.screen,10,40, 150, BAR_HEIGHT, (114,106,133))
		draw_rect(self.screen,10,40, self.player.energy, BAR_HEIGHT, (0,0,225))

	def display_stats(self):
		self.health_bar()
		self.energy_bar()
		#self.screen.blit(self.faceset_image, self.faceset_rect)
		#self.screen.blit(self.ring_image, self.ring_rect)

	def map(self):
		#draw_rect(self.screen, self.map_rect.x - 20, self.map_rect.y - 20, WIDTH * 0.5 + 40, WIDTH * 0.5 + 40, GUI_COLOR)
		self.screen.blit(self.map_image, self.map_rect)
		self.screen.blit(self.frame_image, self.frame_rect)
		
