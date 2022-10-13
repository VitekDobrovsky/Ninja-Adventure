import pyautogui


width, height= pyautogui.size()
WIDTH    = width #* 0.7
HEIGHT   = height #* 0.7

FPS      = 60
TILESIZE = 64


BAR_HEIGHT = 13
FRAME_BAR_HEIGHT = 20


player_stats = {
	'speed': 7,
	'health': 150,
	'energy': 50
}

HITBOX_OFFSET_Y = {
	'player': -26,
	'grass': -20,
	'border': -30,
	'tree': -100,
	'stubbe': -60,
	'border_bridge': 0,
	'border_corner': 20,
	'border_horizontal': 90,
	'border_banister': -63
}

HITBOX_OFFSET_X = {
	'player': 0,
	'grass': -30,
	'border': -50,
	'tree': -50,
	'stubbe': -30,
	'border_bridge': 0,
	'border_corner': 20,
	'border_horizontal': 20,
	'border_banister': 0

}

