#all game settings shouild live in here

TITLE = "Zelda - like"

RESOLUTION = [640, 480]
FPS = 60
TILE_SIZE = 64
TILE_COLLISION = 16

weapon_data = {
    'sword': {'cooldown': 80, 'damage': 15, 'graphic': './gfx/weapons/sword/'},
    'axe': {'cooldown': 150, 'damage': 20, 'graphic': './gfx/weapons/axe/'},
    'lance': {'cooldown': 200, 'damage': 25, 'graphic': './gfx/weapons/lance/'},
    'rapier': {'cooldown': 40, 'damage': 10, 'graphic': './gfx/weapons/rapier/'},
}

# UI settings
BAR_HEIGHT = 5
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 24
UI_FONT = "./gfx/ui/fonts/VT323-Regular.ttf"
UI_FONT_SIZE = 9

#colors

FONT_COLOR = "#D9D2C9"
UI_BG_COLOR = '#323949'

HEALTH_COLOR = '#CD6537'
ENERGY_COLOR = '#53919D'
EXP_POINT_COLOR = '#D0D075'