#
#
#

from typing import Tuple
from src import *

def write(msg: str, color: Tuple[int], pos: Tuple[int], size: int, aa: bool = True, centered: bool = False) -> None:
    font = pygame.font.SysFont("fontawsome", size)
    surface = font.render(msg, aa, color)
    if centered:
        pos = surface.get_rect(center=(pos[0] + pos[2] // 2, pos[1] + pos[3] // 2))
    display.blit(surface, (pos[0], pos[1]))


def translate_pos2idx(pos: Tuple[int]) -> Tuple[int]:
    return ((pos[1] - GRID_POS[1]) // CELL_SIZE[1], (pos[0] - GRID_POS[0]) // CELL_SIZE[0])


def translate_idx2pos(index: Tuple[int], centered: bool = True) -> Tuple[int]:
    return \
        int(centered) * (index[1] * CELL_SIZE[0] + GRID_POS[0] + CELL_SIZE[0]//2, index[0] * CELL_SIZE[1] + GRID_POS[1] + CELL_SIZE[1]//2) + \
        int(not centered) * (index[1] * CELL_SIZE[0] + GRID_POS[0], index[0] * CELL_SIZE[1] + GRID_POS[1])

