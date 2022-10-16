import pygame
from os import walk
from csv import reader

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

# get image from sprite sheet
class Sprite_sheet:
	def __init__(self, path):
		self.sheet = pygame.image.load(path).convert_alpha()

	def get_image(self, col, row):
		image = pygame.Surface((16, 16)).convert_alpha()
		image.blit(self.sheet, (0, 0), ((row * 16), (col * 16), 16, 16))
		image = pygame.transform.scale(image, (64, 64))
		image.set_colorkey((0, 0, 0))
		return image

