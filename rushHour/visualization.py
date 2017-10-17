import pygame
from pygame.locals import *

def run(board, waitTime):

    #set colours with corresponding RGB value
    RED = (255,0,0)
    YELLOW = (255,255,0)
    PINK = (255,0,255)
    GREEN = (0,255,0)
    ORANGE = (255,128,0)
    BLUE = (0,0,255)
    BLACK = (0,0,0)
    BROWN = (153,76,0)
    MAROON = (153,0,0)
    PURPLE = (51,0,110)
    GRAY = (128,128,128)
    MANGENTA = (204,0,102)
    TURQUOISE = (0,255,255)
    WHITE = (255,255,255)

    #set vehicle indexes with corresponding colours
    colours = {
                '0':RED,
                '1':YELLOW,
                '2':PINK,
                '3':GREEN,
                '4':ORANGE,
                '5':BLUE,
                '6':BLACK,
                '7':BROWN,
                '8':MAROON,
                '9':PURPLE,
                '10':GRAY,
                '11':MANGENTA,
                '12':TURQUOISE,
                ' ':WHITE
    }

    #set size of tiles, width and height of grid
    TILESIZE = 40
    GRIDWITDH = 6
    GRIDHEIGHT = 6

    pygame.init()

    #set display
    DISPLAYBOARD = pygame.display.set_mode((GRIDWITDH*TILESIZE, GRIDHEIGHT*TILESIZE))

    #draw rectangles in grid
    for row in range(GRIDHEIGHT):
        for column in range(GRIDWITDH):
            pygame.draw.rect(DISPLAYBOARD, colours[board.state[row][column]], (column*TILESIZE,row*TILESIZE,TILESIZE,TILESIZE))

    #wait 100ms before update
    pygame.time.wait(waitTime)
    pygame.display.update()
