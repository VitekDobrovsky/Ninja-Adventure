import pygame
from support import Sprite_sheet
from item import Item
from settings import *


class Chest(pygame.sprite.Sprite):
	def __init__(self,pos,groups,player,screen, visible_sprites):
		super().__init__(groups)
		
		# images
		self.sheet = Sprite_sheet('graphics/tiles/BigTreasureChest.png', (16, 16), (64, 64))
		self.image = self.sheet.get_image(0,0)
		self.open_chest = self.sheet.get_image(0,4)
		self.frames = [self.sheet.get_image(0,0), self.sheet.get_image(0,1), self.sheet.get_image(0,2), self.sheet.get_image(0,3)]

		# rect
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(-30, HITBOX_OFFSET_Y['chest'])
		self.opening_area = self.rect.inflate(50, 50)
		
		# init
		self.player = player
		self.screen = screen
		self.visible_sprites = visible_sprites

		self.is_open = False
		self.open_index = 0

		self.health_amout = 20
		self.energy_amount = 20

		# energy
		self.energy_image = pygame.image.load('graphics/GUI/energy.png').convert_alpha()
		self.energy_image = pygame.transform.scale(self.energy_image, (BAR_HEIGHT + 7, BAR_HEIGHT + 7))
		self.energy = Item(self.rect.center, [self.energy_image], self.visible_sprites)
		self.p2 = True

		# heart
		self.heart_image = pygame.image.load('graphics/GUI/heart.png').convert_alpha()
		self.heart_image = pygame.transform.scale(self.heart_image, (BAR_HEIGHT + 8, BAR_HEIGHT + 8))
		self.heart = Item(self.rect.center, [self.heart_image], self.visible_sprites)
		self.p1 = True

		# animate
		self.open_time = None
		self.index = 0
		self.animation_speed = 0.1
		self.animation_is_done = False

	def open(self):
		if self.player.hitbox.colliderect(self.opening_area) and self.animation_is_done:
			self.image = self.open_chest
			if self.open_index == 0:
				self.open_time = pygame.time.get_ticks()
				self.is_open = True

	def blit_items(self):
		if self.open_index == 1:
			current_time = pygame.time.get_ticks()
			if current_time - self.open_time >= 250:
				self.heart.items_from_chest(self.player, -1)
			
			self.energy.items_from_chest(self.player, 1)


	def give_content(self):
		if self.is_open:
			self.open_index = 1
			if self.heart.picked or self.energy.picked:
				# give stats
				# TODO: animation
				if self.heart.picked and self.p1:
					self.player.heal_animation = True
					if self.player.health <= 80:
						self.player.health += 20
					else:
						self.player.health += player_stats['health'] - self.player.health
					self.p1 = False

				if self.energy.picked and self.p2:
					self.player.energy_boost_animation = True
					if self.player.energy <= 80:
						self.player.energy += 20
					else:
						self.player.energy += player_stats['energy'] - self.player.energy
					self.p2 = False
	
	def animate(self):
		if self.index <= len(self.frames):
			self.image =  self.frames[int(self.index)]
			self.index += self.animation_speed
		else:
			self.animation_is_done = True

	def update(self):
		self.animate()
		self.blit_items()
		self.open()
		self.give_content()