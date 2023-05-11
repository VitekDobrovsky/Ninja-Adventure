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
			# event handler
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()
					break
			  
			# updating
			self.screen.fill('#71DDEE')
				
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
		reset
	
	GRAPHICS:
		dead sprites
		dead text (and play again) - implwement skull in it

	fix:
		-5 hp bug
		

	OTHER:
		better gameplay
		main menu
'''