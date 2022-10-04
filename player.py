import pygame
from settings import *
from support import import_folder
from support import draw_rect


class Player(pygame.sprite.Sprite):
	def __init__(self, pos, groups, obstacle_sprites):
		super().__init__(groups)
		# set up
		self.image = pygame.image.load('graphics/player/down/down_0.png')
		self.rect = self.image.get_rect(topleft=pos)
		self.hitbox = self.rect.inflate(-6, HITBOX_OFFSET['player'])
		self.screen = pygame.display.get_surface()

		# move
		self.direction = pygame.math.Vector2()
		self.speed = player_stats['speed']

		# colision
		self.obstacle_sprites = obstacle_sprites

		# animation
		self.status = 'down_idle'
		self.pl_assets()
		self.frame_index = 0
		self.frame_speed = 0.15

		# bars
		self.health = player_stats['health']

	def input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_w]:
			self.direction.y = -1
		elif keys[pygame.K_s]:
			self.direction.y = 1
		else:
			self.direction.y = 0

		if keys[pygame.K_d]:
			self.direction.x = 1
		elif keys[pygame.K_a]:
			self.direction.x = -1
		else:
			self.direction.x = 0

	def move(self):
		# normalize direction
		if self.direction.magnitude() != 0:
			self.direction.normalize()

		# apply move
		self.hitbox.x += self.direction.x * self.speed
		self.colision('horizontal')
		self.hitbox.y += self.direction.y * self.speed
		self.colision('vertical')

		# matching hitbox
		self.rect.center = self.hitbox.center

	def colision(self, direction):
		# check horiziontal collision
		if direction == 'horizontal':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.x > 0:
						self.hitbox.right = sprite.hitbox.left
					if self.direction.x < 0:
						self.hitbox.left = sprite.hitbox.right
		# check vertical collision
		elif direction == 'vertical':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.y > 0:
						self.hitbox.bottom = sprite.hitbox.top
					if self.direction.y < 0:
						self.hitbox.top = sprite.hitbox.bottom
		
	def get_status(self):
		# getting y status
		if self.direction.y < 0:
			self.status = 'up'
		elif self.direction.y > 0:
			self.status = 'down'
		else:
			if len(self.status) < 6:
				if self.direction.x == 0:
					self.status += '_idle'
		# getting x status
		if self.direction.x > 0:
			self.status = 'right'
		elif self.direction.x < 0:
			self.status = 'left'
		else:
			if len(self.status) < 6:
				if self.direction.y == 0:
					self.status += '_idle'

	def pl_assets(self):
		character_path = 'graphics/player'
		# store paths
		self.animations = {'up': [],'down': [],'left': [],'right': [],
			'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
			'right_attack':[],'left_attack':[],'up_attack':[],'down_attack':[]} 

		for animation in self.animations.keys():
			full_path = character_path + '/' + animation
			self.animations[animation] = import_folder(full_path)
			
	def animate(self):
		animation = self.animations[self.status]

		self.frame_index += self.frame_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		self.image = animation[int(self.frame_index)]

	def health_bar(self):
		# draw health bar
		draw_rect(self.screen,10 - 2,10 - 2, 204, BAR_HEIGHT + 4, (69,69,69))
		draw_rect(self.screen,10,10, self.health, BAR_HEIGHT, (255,0,0))
		
		# draw energy bar
		draw_rect(self.screen,10 - 2,30 - 2, 204, BAR_HEIGHT + 4, (69,69,69))
		draw_rect(self.screen,10,30, self.health, BAR_HEIGHT, (0,0,225))

	def update(self):
		self.input()
		self.move()
		self.get_status()
		self.animate()
		self.health_bar()