import pyautogui

# window parameters
width, height= pyautogui.size()
WIDTH    = width * 0.9
HEIGHT   = height * 0.9

# set up
FPS      = 60
TILESIZE = 64

# bars
BAR_HEIGHT = 30
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
	'easy' : { 
		'Bamboo': 70,
		'Racoon': 70,
		'Reptile': 80,
		'Spirit_fire': 40
	},
    	'normal' : { 
		'Bamboo': 80,
		'Racoon': 80,
		'Reptile': 90,
		'Spirit_fire': 50
	},
    	'hard' : { 
		'Bamboo': 100,
		'Racoon': 100,
		'Reptile': 110,
		'Spirit_fire': 80
	}
}

ENEMY_DAMAGE = {
    'easy': {
		'Bamboo': 2,
		'Racoon': 5,
		'Reptile': 5,
		'Spirit_fire': 2
        },
    'normal': {
		'Bamboo': 5,
		'Racoon': 7,
		'Reptile': 7,
		'Spirit_fire': 4
        },
    'hard': {
		'Bamboo': 7,
		'Racoon': 13,
		'Reptile': 15,
		'Spirit_fire': 7
        },

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

