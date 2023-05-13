import pygame


class Particle(pygame.sprite.Sprite):
	def __init__(self, player, sheet, visible_sprites, frames_count, type):
		super().__init__()
		self.image = sheet.get_image(0,0)
		self.frames = []

		self.player = player
		self.rect = self.image.get_rect(center=(self.player.rect.centerx, self.player.rect.centery))

		self.visible_sprites = visible_sprites
		self.type = type

		self.add_frames(frames_count, sheet)

		self.added = False

		self.index = 0
		self.animation_speed = 0.15


	def add_frames(self, count, sheet):
		index = 0
		for i in range(count):
			self.frames.append(sheet.get_image(0, index))
			index += 1

	def one_time_animation(self):
		if not self.added:
			self.visible_sprites.add(self)
			self.added = True

		self.rect.center = self.player.rect.center

		if self.index <= len(self.frames):
			if self.type == 'spawn':
				if int(self.index) in (3,4,5):
					self.player.paralized = False
					for image in self.player.frames['down_idle']:
						image.set_alpha(255)
			
			self.image = self.frames[int(self.index)]
			self.index += self.animation_speed
		
		else:
			if self.type == 'health':
				self.player.heal_animation = False
			elif self.type == 'energy':
				self.player.energy_boost_animation = False
			elif self.type == 'spawn':
				self.player.spawning = False
			self.added = False
			self.index = 0
			self.visible_sprites.remove(self)


