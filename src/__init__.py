


import math
import time
import random
import warnings
import pygame


pygame.init()
pygame.font.init()
display_width, display_height = (1440, 810)
display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

