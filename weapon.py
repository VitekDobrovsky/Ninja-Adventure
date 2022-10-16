import pygame

class Weapon(pygame.sprite.Sprite):
	def __init__(self, player_rect, player_status, visible_sprites):
		super().__init__()
		# init
		self.status = player_status
		self.player_rect = player_rect
		self.screen = pygame.display.get_surface()
		self.visible_sprites = visible_sprites

		# define image and rect
		self.image = pygame.transform.scale(pygame.image.load('graphics/weapons/sword.png').convert_alpha(), (22,40))
		self.down = self.image
		self.up = pygame.transform.rotate(self.image, 180)
		self.right = pygame.transform.rotate(self.image, 90)
		self.left = pygame.transform.rotate(self.image, 270)
		self.image = pygame.transform.scale(self.image, (18,33))
		self.rect = self.image.get_rect()

	def show(self):
		# matching image by status
		if self.status == 'down_attack':
			self.image = self.down
			self.rect = self.image.get_rect(topleft=(self.player_rect.bottomleft[0] + 0, self.player_rect.bottomleft[1]))
		elif self.status == 'up_attack':
			self.image = self.up
			self.rect = self.image.get_rect(bottomleft=(self.player_rect.topleft[0] + 9, self.player_rect.topleft[1]))
		elif self.status == 'left_attack':
			self.image = self.left 
			self.rect = self.image.get_rect(bottomright=(self.player_rect.bottomleft[0], self.player_rect.bottomleft[1] - 5))
		elif self.status == 'right_attack':
			self.image = self.right
			self.rect = self.image.get_rect(bottomleft=(self.player_rect.bottomright[0], self.player_rect.bottomright[1] - 5))

		# draw weapon
		self.visible_sprites.add(self)

	def remove(self):
		# remove weapon
		self.visible_sprites.remove(self)
	


	