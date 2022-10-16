#all game settings shouild live in here
from enum import Enum

TITLE = "Zelda - like"

RESOLUTION = [512, 320]
FPS = 60
TILE_SIZE = 16
TILE_COLLISION = 16
RENDER_DIST = 340

#weapons
weapon_data = {
    'sword': {'cooldown': 80, 'damage': 15, 'graphic': './gfx/weapons/sword/'},
    'axe': {'cooldown': 150, 'damage': 20, 'graphic': './gfx/weapons/axe/'},
    'lance': {'cooldown': 200, 'damage': 25, 'graphic': './gfx/weapons/lance/'},
    'rapier': {'cooldown': 40, 'damage': 10, 'graphic': './gfx/weapons/rapier/'},
}

#magic
magic_data = {
    'flame': {'strength': 5, 'cost': 20, 'graphic': './gfx/magic/flame/'},
    'heal': {'strength': 15, 'cost': 20, 'graphic': './gfx/magic/heal/'}
}



# UI settings
BAR_HEIGHT = 4
HEALTH_BAR_WIDTH = 114
ENERGY_BAR_WIDTH = 101
EXP_BAR_WIDTH = 112
ITEM_BOX_SIZE = 24
UI_FONT = "./gfx/ui/fonts/VT323-Regular.ttf"
UI_FONT_SIZE = 9

#colors

FONT_COLOR = "#D9D2C9"
UI_BG_COLOR = '#323949'

HEALTH_COLOR = '#E86633'
ENERGY_COLOR = '#1ECAEB'
EXP_POINT_COLOR = '#D0D075'
BAR_BG_COLOR = '#4F4F50'

class State(Enum):
    MOVE = 1
    ATTACK = 2
    DEAD = 3
    FOLLOW = 4
    HURT = 5