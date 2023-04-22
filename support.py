import pygame
from os import walk
from csv import reader
from math import sin

# get multiple images from folder
def  import_folder(path):
	img_list = []
	for _,__,img_files in walk(path):
		for image in img_files:
			full_path = path + '/' + image
			image_surface = pygame.image.load(full_path).convert_alpha()
			img_list.append(image_surface)
	return img_list

# edit csv files to map create algorythm
def import_csv_layout(path):
	terrain_map = []
	with open(path) as level_map:
		layout = reader(level_map,delimiter = ',')
		for row in layout:
			terrain_map.append(list(row))
		return terrain_map

# draw rect
def draw_surface(screen,x,y,width,height,color, alpha):
	surface = pygame.Surface((width, height))
	surface.fill(color)
	surface.set_alpha(alpha)
	rect = surface.get_rect(topleft=(x,y))
	screen.blit(surface, rect)

def draw_rect(screen,x,y,width,height,color):
	rect = pygame.Rect(x,y,width,height)
	pygame.draw.rect(screen, color, rect)

# debug
def debug(value, screen):
	font = pygame.font.Font('graphics/fonts/font.ttf' ,50)
	text = font.render(value,True, (225,225,225))
	rect = text.get_rect(topleft=(0,500))
	pygame.draw.rect(screen, (0,0,0), rect)
	screen.blit(text, rect)

# text
class Text:
	def __init__(self, screen, text, path, size, pos, color):
		self.screen = screen
		font = pygame.font.Font(path, size)
		self.text_surf = font.render(text, True, color)
		self.text_rect = self.text_surf.get_rect(center = pos)

	def draw(self):
		self.screen.blit(self.text_surf, self.text_rect)

# get image from sprite sheet
class Sprite_sheet:
	def __init__(self, path, index, size):
		self.sheet = pygame.image.load(path).convert_alpha()
		self.index = index
		self.size = size

	def get_image(self, col, row):
		image = pygame.Surface(self.index).convert_alpha()
		image.blit(self.sheet, (0, 0), ((row * self.index[0]), (col * self.index[1]), self.index[0], self.index[1]))
		image = pygame.transform.scale(image, self.size)
		image.set_colorkey((0, 0, 0))
		return image

