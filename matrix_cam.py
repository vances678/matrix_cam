import pygame as pg
import numpy as np
import cv2 as cv

def get_prerendered_chars():
    char_colors = [(0, green, 0) for green in range(256)]
    prerendered_chars = {}
    for char in characters:
        prerendered_char = {(char, color): font.render(char, True, color) for color in char_colors}
        prerendered_chars.update(prerendered_char)
    return prerendered_chars

# pygame/frame init
res = width, height = 1440, 900
pg.init()
screen = pg.display.set_mode(res)
surface = pg.Surface(res)

# camera init
cam = cv.VideoCapture(0)

# matrix init
font_size = 14
font = pg.font.Font('font/ms mincho.ttf', font_size, bold=True)
size = rows, cols = height // font_size, width // font_size
katakana = '0x30a0'
greek = '0x0370'
russian = '0x0400'
arabic = '0x0600'
math = '0x2200'
normal = '0x0000'
matrix_chars = '0 1 2 3 4 5 7 8 9 Z : ・ . " = * + - < > ¦ ｜ ╌ ﾊ ﾐ ﾋ ｰ ｳ ｼ ﾅ ﾓ ﾆ ｻ ﾜ ﾂ ｵ ﾘ ｱ ﾎ ﾃ ﾏ ｹ ﾒ ｴ ｶ ｷ ﾑ ﾕ ﾗ ｾ ﾈ ｽ ﾀ ﾇ ﾍ'.split(' ')
characters =  np.array(matrix_chars + ['' for i in range(10)])
#characters = np.array([chr(int(katakana, 16) + i) for i in range(96)] + ['' for i in range(10)])

matrix = np.random.choice(characters, size)
char_intervals = np.random.randint(25, 50, size=size)
cols_speed = np.random.randint(1, 500, size=size)
prerendered_chars = get_prerendered_chars()

def change_chars(frames):
    mask = np.argwhere(frames % char_intervals == 0)
    new_chars = np.random.choice(characters, mask.shape[0])
    matrix[mask[:, 0], mask[:, 1]] = new_chars

def shift_column(frames):
    num_cols = np.argwhere(frames % cols_speed == 0)
    num_cols = num_cols[:, 1]
    num_cols = np.unique(num_cols)
    matrix[:, num_cols] = np.roll(matrix[:, num_cols], shift = 1, axis = 0)

while True:
    [exit() for i in pg.event.get() if i.type == pg.QUIT or i.type == pg.KEYDOWN ]

    # set to black to erase previous frames of characters
    surface.fill(pg.Color('black'))

    # camera stuff
    check, oppositeCamImage = cam.read()
    camImage = cv.flip(oppositeCamImage, 1)
    pgImage = pg.image.frombuffer(camImage.tobytes(), camImage.shape[1::-1], "RGB")

    cam_surface = pg.Surface((1280, 720))
    cam_surface.blit(pgImage, (0, 0))
    
    image = pg.transform.scale(cam_surface, res)
    pixel_array = pg.pixelarray.PixelArray(image)

    # matrix stuff
    frames = pg.time.get_ticks() 
    change_chars(frames)
    shift_column(frames)
    
    for y, row in enumerate(matrix):
        for x, char in enumerate(row):
            if char:
                pos = x * font_size, y * font_size
                _, red, green, blue = pg.Color(pixel_array[pos])
                if red and green and blue:
                    color = (red + green + blue) // 3
                    color = 255 - color # comment this line to invert
                    color = 220 if 160 < color < 220 else color
                    char = prerendered_chars[(char, (0, color, 0))]
                    char.set_alpha(color)
                    surface.blit(char, pos)    

    # display
    screen.blit(surface, (0,0))
    pg.display.flip()

    
