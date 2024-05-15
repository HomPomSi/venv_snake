# @author   LukasGruenwald
# @version  2024.15.05
# @description
#   Setup constants/variables needed in almost every file
#   Initialize pygame modules (main, clock, timer etc.)



#---------------------------------------------------------------------------------------------------
# Imports needed in almost all files
import math
import time
import random
import warnings
import pygame



#---------------------------------------------------------------------------------------------------
# Pygame init
pygame.init()
pygame.font.init()
display_width, display_height = (1440, 810)
display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)



#---------------------------------------------------------------------------------------------------
# Constants, Variables

# Top left corner position in px
GRID_POS = (100, 100)

# Number of rows/columns
GRID_SIZE = (19, 32)

# Cell dimensions in px
CELL_SIZE = (32, 32)

# Rectangle of grid (x,y,w,h), notice the oppsite indices of grid/cell size because
# grid is sized in row/col and cell is sized in px_width, px_height
GRID_RECT = (
    *GRID_POS, 
    GRID_SIZE[1] * CELL_SIZE[0], 
    GRID_SIZE[0] * CELL_SIZE[1]
)

# Amount of 1/N updates per second
SNAKE_SPEED = 8 

# Width of the snake body in px
SNAKE_SIZE = (CELL_SIZE[0]//2, CELL_SIZE[1]//2)

# Maximum number of fruits on the grid at the same time
FRUITS_MAX = 8
