import pygame
from support import draw_rect, Text
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

		# heart
		self.heart_image = pygame.image.load('graphics/GUI/heart.png').convert_alpha()
		self.heart_image = pygame.transform.scale(self.heart_image, (BAR_HEIGHT + 8, BAR_HEIGHT + 8))
		self.heart_image.set_colorkey((20, 27, 27))
		self.hear_rect = self.heart_image.get_rect(topleft = (5, 5))

		# energy symbol
		self.energy_image = pygame.image.load('graphics/GUI/energy.png').convert_alpha()
		self.energy_image = pygame.transform.scale(self.energy_image, (BAR_HEIGHT + 7, BAR_HEIGHT + 7))
		self.energy_image.set_colorkey((20, 27, 27))
		self.energy_rect = self.energy_image.get_rect(topleft = (5, 38))

	def health_bar(self):
		# draw health bar
		draw_rect(self.screen,37,7, 306, BAR_HEIGHT + 6, '#FDD503')
		draw_rect(self.screen,40,10, 300, BAR_HEIGHT, (133, 106, 106))
		draw_rect(self.screen,40,10, self.player.health * 3 , BAR_HEIGHT, (255,0,0))

		Text(self.screen, f'{round(self.player.health)}/100', 'graphics/fonts/Gameplay.ttf', 15, (160, 20), 'white').draw()
		self.screen.blit(self.heart_image, self.hear_rect)
		
	def energy_bar(self):
		# draw energy bar
		draw_rect(self.screen,37,37, 156, BAR_HEIGHT + 6, '#A4A7A8')
		draw_rect(self.screen,40,40, 150, BAR_HEIGHT, (114,106,133))
		draw_rect(self.screen,40,40, self.player.energy * 1.5, BAR_HEIGHT, (0,0,225))

		self.screen.blit(self.energy_image, self.energy_rect)

	def display_stats(self):
		self.health_bar()
		self.energy_bar()
		#self.screen.blit(self.faceset_image, self.faceset_rect)
		#self.screen.blit(self.ring_image, self.ring_rect)

	def map(self):
		#draw_rect(self.screen, self.map_rect.x - 20, self.map_rect.y - 20, WIDTH * 0.5 + 40, WIDTH * 0.5 + 40, GUI_COLOR)
		self.screen.blit(self.map_image, self.map_rect)
		self.screen.blit(self.frame_image, self.frame_rect)
		
