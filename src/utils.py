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
    return ((pos[1] - 100) // 32, (pos[0] - 100) // 32)


def translate_idx2pos(index: Tuple[int]) -> Tuple[int]:
    return (index[1] * 32 + 100 + 16, index[0] * 32 + 100 + 16)

