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
	1. fix enemy collision
	2. push enemy after attack
	3. get damage
	4. minus energy
	5. better stats bars
	6. baricade animation
	7. blickering after damage to enemy
	8. enemy dead animation
	8. aim assist
'''
