#
#
#

from src import *
from src.enums import Direction
from src.utils import translate_idx2pos, translate_pos2idx
from src.color import Color
from typing import Tuple, List
from src.consumables import *



class PartInfo(object):
    def __init__(self, pos, into, to) -> None:
        self.pos = pos
        self.into = into
        self.to = to



class Snake(object):
    "POSITIONS are handled as index"
    head_image = pygame.image.load("resources/snake_head.png")
    body_image = pygame.image.load("resources/snake_body.png")
    def __init__(self, parts: List[Tuple[PartInfo]], direction: Direction = Direction.EAST) -> None:
        self.parts: List[Tuple[PartInfo]] = parts
        self.direction = direction
        self.pause = 0

    def get_size(self) -> int:
        return len(self.parts)

    def eat(self, consumable: Consumable) -> None:
        print(f"Eating {str(consumable)}")
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
        self.parts.append(PartInfo(((self.parts[-1].pos[0] + direction.value[0])%19, (self.parts[-1].pos[1] + direction.value[1])%32), self.direction, direction))
        if len(self.parts) >= 2:
            self.parts[-2].to = self.direction
        if self.pause <= 0:
            del self.parts[0]
        else:
            self.pause -= 1

    def draw(self) -> None:
        for index, part in enumerate(self.parts):
            pos = translate_idx2pos(part.pos)
            if index == len(self.parts) - 1:
                display.blit(pygame.transform.rotate(Snake.head_image, self.direction.value[2] * 90), (pos[0] - 16, pos[1] - 16))
            elif index == 0:
                match part.to:
                    case Direction.EAST:
                        pygame.draw.rect(display, Color.GREEN, (pos[0] - 8, pos[1] - 8, 23, 16), 0)
                    case Direction.SOUTH:
                        pygame.draw.rect(display, Color.GREEN, (pos[0] - 8, pos[1] - 8, 16, 23), 0)
                    case Direction.WEST:
                        pygame.draw.rect(display, Color.GREEN, (pos[0] - 15, pos[1] - 8, 23, 16), 0)
                    case Direction.NORTH:
                        pygame.draw.rect(display, Color.GREEN, (pos[0] - 8, pos[1] - 15, 16, 23), 0)
            else:
                self._draw_part(part)
   

    def _draw_part(self, part: PartInfo) -> None:
        pos = translate_idx2pos(part.pos)
        
        if part.into == part.to:
            if part.into.value[0] == 0:
                pygame.draw.rect(display, Color.GREEN, (pos[0]-15, pos[1]-8, 30, 16), 0)
            else:
                pygame.draw.rect(display, Color.GREEN, (pos[0]-8, pos[1]-15, 16, 30), 0)

        # works for clockwise
        match (part.into, part.to):
            case (Direction.SOUTH, Direction.EAST):
                pygame.draw.rect(display, Color.GREEN, (pos[0] - 8, pos[1] - 8, 23, 16), 0)
                pygame.draw.rect(display, Color.GREEN, (pos[0] - 8, pos[1] - 15, 16, 23), 0)

            case (Direction.SOUTH, Direction.WEST):
                pygame.draw.rect(display, Color.GREEN, (pos[0] - 15, pos[1] - 8, 23, 16), 0)
                pygame.draw.rect(display, Color.GREEN, (pos[0] - 8, pos[1] - 15, 16, 23), 0)

            case (Direction.NORTH, Direction.EAST):
                pygame.draw.rect(display, Color.GREEN, (pos[0] - 8, pos[1] - 8, 23, 16), 0)
                pygame.draw.rect(display, Color.GREEN, (pos[0] - 8, pos[1] - 8, 16, 23), 0)

            case (Direction.NORTH, Direction.WEST):
                pygame.draw.rect(display, Color.GREEN, (pos[0] - 15, pos[1] - 8, 23, 16), 0)
                pygame.draw.rect(display, Color.GREEN, (pos[0] - 8, pos[1] - 8, 16, 23), 0)

            case (Direction.EAST, Direction.NORTH):
                pygame.draw.rect(display, Color.GREEN, (pos[0] - 15, pos[1] - 8, 23, 16), 0)
                pygame.draw.rect(display, Color.GREEN, (pos[0] - 8, pos[1] - 15, 16, 23), 0)
            
            case (Direction.EAST, Direction.SOUTH):
                pygame.draw.rect(display, Color.GREEN, (pos[0] - 15, pos[1] - 8, 23, 16), 0)
                pygame.draw.rect(display, Color.GREEN, (pos[0] - 8, pos[1] - 8, 16, 23), 0)
            
            case (Direction.WEST, Direction.NORTH):
                pygame.draw.rect(display, Color.GREEN, (pos[0] - 8, pos[1] - 8, 23, 16), 0)
                pygame.draw.rect(display, Color.GREEN, (pos[0] - 8, pos[1] - 15, 16, 23), 0)
            
            case (Direction.WEST, Direction.SOUTH):
                pygame.draw.rect(display, Color.GREEN, (pos[0] - 8, pos[1] - 8, 23, 16), 0)
                pygame.draw.rect(display, Color.GREEN, (pos[0] - 8, pos[1] - 8, 16, 23), 0)



