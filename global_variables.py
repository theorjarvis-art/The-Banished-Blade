# ---------- Global Variables ---------- #
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILESIZE = 32
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PLAYER_SPEED = 300
PLAYER_SCALE = 1.5

# ------------ animation settings ---------------- #

PLAYER_SHEET = "assets/player_sheet.png"   # path to  sprite sheet
FRAME_W = 32                               # width of one frame in pixels
FRAME_H = 32                               # height of one frame in pixels
FRAMES_PER_ROW = 4                         # walking frames per direction
ANIM_TIME = 0.12                           # seconds each frame is shown

# Which row of the sheet holds each direction
ROW_DOWN = 0
ROW_LEFT = 1
ROW_RIGHT = 2
ROW_UP = 3