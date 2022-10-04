import pygame
from os import walk


def  import_folder(path):
	img_list = []
	for _,__,img_files in walk(path):
		for image in img_files:
			full_path = path + '/' + image
			image_surface = pygame.image.load(full_path).convert_alpha()
			img_list.append(image_surface)
	return img_list

def draw_rect(screen,x,y,width,height,color):
	rect = pygame.Rect(x,y,width,height)
	pygame.draw.rect(screen, color, rect)