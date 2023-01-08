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
	GUI
	boss
	damage animation
	picking coin animation
	no energy text
	screen shake
	animate clear text
	optimate clear text
	optimization of gameplay
	animate more things
	better shards and heart graphics
	better chest animation = stuf to floor
	more levels
'''
