import pygame
from sys import exit
from settings import *
from level import Level
from support import Sprite_sheet
from support import Button
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
		for i in range(5):
			self.heading_frames.append(self.heading_sheet.get_image(index,0))
			index += 1
		
		self.space_pressed = False

		self.heading_index = 0
		self.heding_speed = 0.05

		self.heading = self.heading_frames[0]
		self.heading_rect =self.heading.get_rect(center=(WIDTH / 2, HEIGHT / 7))
		self.heading.set_alpha(0)

		self.want_play = False
		self.want_play_time = None

		# sin wave motion
		self.r = 10
		self.theta = 0

		self.font = pygame.font.Font('graphics/fonts/Gameplay.ttf' ,40)
		self.play_txt = self.font.render('press SPACE to play!',True, (225,225,225))
		self.play_rect = self.play_txt.get_rect(center=(WIDTH / 2, HEIGHT /2))
		self.play_alpha = 0
		self.play_txt.set_alpha(0)

		# choose difficulty
		self.dificulty_txt  = self.font.render('Set dificulty:', True, (225,225,225))
		self.dificulty_txt = pygame.transform.scale(self.dificulty_txt, (self.dificulty_txt.get_width() * 0.7, self.dificulty_txt.get_height() *0.7))
		self.dificulty_rect = self.dificulty_txt.get_rect(center= (WIDTH / 2, HEIGHT * 0.6))

		self.dificulty = 'normal'
		
		self.font = pygame.font.Font('graphics/fonts/Gameplay.ttf' ,20)
		self.easy = Button(self.font,'easy',(self.dificulty_rect.centerx,self.dificulty_rect.centery + 50),(255,255,255),'white')
		self.normal = Button(self.font,'normal',(self.dificulty_rect.centerx,self.dificulty_rect.centery + 100),(255,255,255),'white')
		self.hard = Button(self.font,'hard',(self.dificulty_rect.centerx,self.dificulty_rect.centery + 150),(255,255,255),'white')

		self.dif_types = [self.easy, self.normal, self.hard]

	def dificulties(self):

		for dif in self.dif_types:
			if dif.area.collidepoint(pygame.mouse.get_pos()):
				if pygame.mouse.get_pressed()[0]:		
					self.dificulty = dif.str	

		if self.dificulty == 'easy':
			self.easy.selected = True
			self.normal.selected = False
			self.hard.selected = False
		elif self.dificulty == 'normal':
			self.easy.selected = False
			self.normal.selected = True
			self.hard.selected = False
		elif self.dificulty == 'hard':
			self.easy.selected = False
			self.normal.selected = False
			self.hard.selected = True

	def main_menu(self):
		if int(self.heading_index) <= 2:
			self.heading.set_alpha(255)
			self.play_txt.set_alpha(self.play_alpha)
			self.play_alpha += 7
			self.heading = self.heading_frames[int(self.heading_index)]
			self.heading_index += self.heding_speed
		
		if self.want_play:
			if int(self.heading_index) >= 2:
				if int(self.heading_index) <= 3:
					self.heading_index += self.heding_speed
					self.heading = self.heading_frames[int(self.heading_index)]
					self.play_alpha -= 30
					self.play_txt.set_alpha(self.play_alpha)
				else:
					self.heading.set_alpha(0)

			
			
			if pygame.time.get_ticks() - self.want_play_time >= 700:
				self.in_main_menu = False

		self.heading_rect.y = (HEIGHT / 6) + self.r * sin(0.1 * self.theta)
		self.theta += 0.3
		self.screen.blit(self.heading, self.heading_rect)
		self.screen.blit(self.play_txt, self.play_rect)
		self.screen.blit(self.dificulty_txt, self.dificulty_rect)
		self.dificulties()
		self.easy.render(self.screen)
		self.normal.render(self.screen)
		self.hard.render(self.screen)

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
				if self.in_main_menu and not self.space_pressed:
					self.want_play_time = pygame.time.get_ticks()
					self.want_play = True
					self.space_pressed = True
			
			# updating
			self.screen.fill('#4ca5b5')
			if self.in_main_menu:
				self.main_menu()
			else:
				# restart game
				if not self.level.player.restart:
					self.level.run(self.dificulty)
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
		pause menu
		chose diferent font to play again text and center it
'''