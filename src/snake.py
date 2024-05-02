#
#
#

from src import *
from src.enums import Direction
from src.utils import translate_idx2pos, translate_pos2idx
from typing import Tuple, List
from src.consumables import *

class Snake(object):
    "POSITIONS are handled as index"
    head_image = pygame.image.load("resources/snake_head.png")
    body_image = pygame.image.load("resources/snake_body.png")
    def __init__(self, parts: List[Tuple[int]], direction: Direction = Direction.EAST) -> None:
        self.parts: List[Tuple[int]] = parts
        self.direction = direction
        self.pause = 0

    def get_size(self) -> int:
        return len(self.parts)

    def eat(self, consumable: Consumable) -> None:
        print(f"Eating {consumable.__class__}")
        value = consumable.consume()
        if value > 0:
            self.grow(value)
        else:
            self.shrink(-value)

    def grow(self, size: int = 1) -> None:
        self.pause += size

    def shrink(self, size: int) -> None:
        if size >= len(self.parts):
            raise GameOverException("Snake starved to Death")
        self.parts = self.parts[size:]

    def update(self, direction: Direction) -> None:
        # Do not change direction when new direction point into opposite direction
        if self.direction.value[0] + direction.value[0] == 0 and self.direction.value[1] + direction.value[1] == 0:
            direction = self.direction
        self.direction = direction
        self.parts.append(((self.parts[-1][0] + direction.value[0])%19, (self.parts[-1][1] + direction.value[1])%32))
        if self.pause <= 0:
            del self.parts[0]
        else:
            self.pause -= 1

    def draw(self) -> None:
        for index, part in enumerate(self.parts):
            pos = translate_idx2pos(part)
            if index == len(self.parts) - 1:
                display.blit(pygame.transform.rotate(Snake.head_image, self.direction.value[2] * 90), (pos[0] - 16, pos[1] - 16))
            elif index == 0:
                pygame.draw.circle(display, 0x12e012, translate_idx2pos(part), 16, 0)
            else:
                pygame.draw.circle(display, 0x12e012, translate_idx2pos(part), 16, 0)
                #display.blit(pygame.transform.rotate(Snake.body_image, self.direction.value[2] * 90), (pos[0] - 16, pos[1] - 16))

