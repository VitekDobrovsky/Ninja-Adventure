import pygame
from sys import exit
from settings import *


class Game:
	def __init__(self):
		# set up
		pygame.init()
		pygame.display.set_caption('Game')
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
		self.clock = pygame.time.Clock()

	def run(self):
		# main loop
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()
					break
			
			# updating
			self.screen.fill('black')
			pygame.display.update()
			self.clock.tick(FPS)


if __name__ == '__main__':
	game = Game()
	game.run()
