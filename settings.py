import pyautogui

# window parameters
width, height= pyautogui.size()
WIDTH    = width * 0.9
HEIGHT   = height * 0.9

# set up
FPS      = 60
TILESIZE = 64

# bars
BAR_HEIGHT = 20
FRAME_BAR_HEIGHT = 20

# COLOR
RED_TEXT = '#FFD700'
GUI_COLOR = '#FFD700'

# player stats
player_stats = {
	'speed': 7,
	'health': 100,
	'energy': 100
}

# enemies
ENEMY_HEALTH = {
	'Bamboo': 90,
	'Racoon': 90,
	'Reptile': 120,
	'Spirit_fire': 60
}

ENEMY_DAMAGE = {
	'Bamboo': 5,
	'Racoon': 10,
	'Reptile': 15,
	'Spirit_fire': 5
}


# hitboxes inflations
HITBOX_OFFSET_Y = {
	'player': -26,
	'enemy': -26,
	'grass': -20,
	'border': -30,
	'tree': -100,
	'stubbe': -60,
	'border_bridge': 0,
	'border_corner': 20,
	'border_horizontal': 90,
	'border_banister': -63,
	'baricade_vertical': 0,
	'baricade_horizontal': 0,
	'chest': -50
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
	'border_banister': 0,
	'baricade_vertical': 0,
	'baricade_horizontal': 0

}

