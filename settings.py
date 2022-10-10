import pyautogui


width, height= pyautogui.size()
WIDTH    = width * 0.7
HEIGHT   = height * 0.7

FPS      = 60
TILESIZE = 64


BAR_HEIGHT = 13
FRAME_BAR_HEIGHT = 20


player_stats = {
	'speed': 7,
	'health': 150,
	'energy': 50
}

HITBOX_OFFSET = {
	'player': -26,
	'grass': -20,
	'border': -30
}
