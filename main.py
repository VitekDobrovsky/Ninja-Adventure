import pygame
from sys import exit
from settings import *
from level import Level


class NinjaAdventure:
	def __init__(self):
		# set up
		pygame.init()
		pygame.font.init()
		pygame.display.set_caption('Ninja Adventure')
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
		self.clock = pygame.time.Clock()  
		self.level = Level()
  
	def run(self):
		# main loop
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()
					break
			
			# updating
			self.screen.fill('#71DDEE')
			self.level.run()
			pygame.display.update()
			self.clock.tick(FPS)


if __name__ == '__main__':
	game = NinjaAdventure()
	game.run()

'''
TODO:
	better stats bars
	minimap
	more weapons
	weapon gui
	aim assist
	boss
	convert all to sprite sheets
	damage animation
	change size of gui
	optimate clear text
	clean up level
	animate more things
'''
# BUGS:
# not switching weapons properly