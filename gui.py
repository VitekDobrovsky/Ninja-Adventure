import pygame
from support import draw_rect, Text
from settings import *


class GUI:
	def __init__(self, player):
		self.screen = pygame.display.get_surface()
		self.player = player

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
		self.energy_rect = self.energy_image.get_rect(topleft = (5, 48))

		# coins
		self.coin_image = pygame.image.load('graphics/GUI/coin.png').convert_alpha()
		self.coin_image = pygame.transform.scale(self.coin_image, (BAR_HEIGHT + 5, BAR_HEIGHT + 5))
		self.coin_image.set_colorkey((20, 27, 27))
		self.coin_rect = self.coin_image.get_rect(topleft= (5, 84))

		# 'no energy' text
		self.t_noenergy_image = pygame.image.load('graphics/GUI/no_energy_text.png').convert_alpha()
		self.t_noenergy_image = pygame.transform.scale2x(self.t_noenergy_image)
		self.t_noenergy_image = pygame.transform.scale2x(self.t_noenergy_image)
		self.t_noenergy_rect = self.t_noenergy_image.get_rect(center= (WIDTH / 2, HEIGHT - 50))
		self.t_noenergy_show = False
		self.t_noenergy_time = None

	def health_bar(self):
		# draw health bar
		draw_rect(self.screen,42,7, 306, BAR_HEIGHT + 6, '#FDD503')
		draw_rect(self.screen,45,10, 300, BAR_HEIGHT, (133, 106, 106))
		draw_rect(self.screen,45,10, self.player.health * 3 , BAR_HEIGHT, (255,0,0))

		Text(self.screen, f'{round(self.player.health)}/100', 'graphics/fonts/Gameplay.ttf', 15, (160, 25), 'white').draw()
		self.screen.blit(self.heart_image, self.hear_rect)
		
	def energy_bar(self):
		# draw energy bar
		draw_rect(self.screen,42,47, 156, BAR_HEIGHT + 6, '#A4A7A8')
		draw_rect(self.screen,45,50, 150, BAR_HEIGHT, (114,106,133))
		draw_rect(self.screen,45,50, self.player.energy * 1.5, BAR_HEIGHT, (0,0,225))

		self.screen.blit(self.energy_image, self.energy_rect)

	def coins(self):
		self.screen.blit(self.coin_image, self.coin_rect)
		Text(self.screen, str(self.player.coins), 'graphics/fonts/Gameplay.ttf', 25, (55, 100), 'white').draw()

	def t_noenergy(self):
		current_time = pygame.time.get_ticks()
		keys = pygame.key.get_pressed()
		if self.player.energy < 1:
			if keys[pygame.K_SPACE]:
				#self.t_noenergy_time = pygame.time.get_ticks()
				#self.t_noenergy_show = True
				pass

		if self.t_noenergy_show:
			self.screen.blit(self.t_noenergy_image, self.t_noenergy_rect)

		# cooldown
		if self.t_noenergy_show:
			if current_time - self.t_noenergy_time > 500:
				self.t_noenergy_show = False

		if keys[pygame.K_SPACE] and self.player.energy <= 5 and self.player.can_attack:
			self.t_noenergy_time = pygame.time.get_ticks()
			self.t_noenergy_show = True

	def display_stats(self):
		self.health_bar()
		self.energy_bar()
		self.coins()
		self.t_noenergy()
		
