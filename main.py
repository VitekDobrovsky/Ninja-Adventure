import pygame
from sys import exit
from settings import *
from level import Level
from support import Sprite_sheet
from math import sin

class NinjaAdventure:
	def __init__(self):
		# set up
		pygame.init()
		pygame.font.init()
		pygame.display.set_caption('Ninja Adventure')

		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
		self.clock = pygame.time.Clock()  
		self.level = Level()

		# main menu
		self.in_main_menu = True
		self.heading_sheet = Sprite_sheet('graphics/GUI/NinjaAdventure2.png', (117, 25), ((72 * 10, 25 * 6)))
		self.heading_frames = []
		index = 0
		for i in range(4):
			self.heading_frames.append(self.heading_sheet.get_image(index,0))
			index += 1

		self.heading_index = 0
		self.heding_speed = 0.05

		self.heading = self.heading_frames[0]
		self.heading_rect =self.heading.get_rect(center=(WIDTH / 2, HEIGHT / 7))
		self.heading.set_alpha(0)

		# sin wave motion
		self.r = 10
		self.theta = 0

		self.font = pygame.font.Font('graphics/fonts/Gameplay.ttf' ,40)
		self.play_txt = self.font.render('press SPACE to play!',True, (225,225,225))
		self.play_rect = self.play_txt.get_rect(center=(WIDTH / 2, HEIGHT /2))

	def main_menu(self):
		if int(self.heading_index) <= 2:
			self.heading.set_alpha(255)
			self.heading = self.heading_frames[int(self.heading_index)]
			self.heading_index += self.heding_speed
		
		self.heading_rect.y = (HEIGHT / 6) + self.r * sin(0.1 * self.theta)
		self.theta += 0.3
		self.screen.blit(self.heading, self.heading_rect)
		self.screen.blit(self.play_txt, self.play_rect)

	def run(self):
		# main loop
		while True:
			# event handler
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()
					break
			  
			if pygame.key.get_pressed()[pygame.K_SPACE]:
				if self.in_main_menu:
					self.in_main_menu = False
			# updating
			self.screen.fill('#4ca5b5')
			if self.in_main_menu:
				self.main_menu()
			else:
				# restart game
				if not self.level.player.restart:
					self.level.run()
				else:
					self.level = Level()

			

			pygame.display.update()
			self.clock.tick(FPS)


if __name__ == '__main__':
	game = NinjaAdventure()
	game.run()

'''
TODO:
	ANIMATE:
		taking damage
		enemy attack
		kill bush
		death
	
	GRAPHICS:
		dead sprites
		dead text (and play again) - implement skull in it

	fix:
		-5 hp bug
		fix that you can restart immediately after death
		and animate after restartw

	OTHER:
		better gameplay
		pause menu
		main menu
		get rid of other weapon
		chose diferent font to play again text and center it
'''