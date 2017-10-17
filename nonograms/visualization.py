import pygame
from pygame.locals import *

def run(nonogram, waitTime):

    #set colours with corresponding RGB value
    BLACK = (0,0,0)
    WHITE = (255,255,255)

    #set vehicle indexes with corresponding colours
    colours = {
                'X':BLACK,
                ' ':WHITE
    }

    #set size of tiles, width and height of grid
    TILESIZE = 40
    GRIDWITDH = nonogram.dimensions[0]
    GRIDHEIGHT = nonogram.dimensions[1]

    pygame.init()

    #set display
    DISPLAYNONOGRAM = pygame.display.set_mode((GRIDWITDH*TILESIZE, GRIDHEIGHT*TILESIZE))

    #draw rectangles in grid
    for row in range(GRIDHEIGHT):
        for column in range(GRIDWITDH):
            pygame.draw.rect(DISPLAYNONOGRAM, colours[nonogram.state[row][column]], (column*TILESIZE,row*TILESIZE,TILESIZE,TILESIZE))

    #wait 100ms before update
    #pygame.time.wait(0)
    pygame.display.update()
    pygame.time.wait(waitTime)
