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
    
    def __repr__(self) -> str:
        return f"{self.pos}: {self.into} -> {self.to}"


class Snake(object):
    "POSITIONS are handled as index"
    head_image = pygame.image.load("resources/snake_head.png")
    body_image = pygame.image.load("resources/snake_body.png")
    def __init__(self, parts: List[Tuple[PartInfo]], direction: Direction = Direction.EAST) -> None:
        self.parts: List[Tuple[PartInfo]] = parts
        self._direction = direction
        self.pause = 0
    
    @property
    def direction(self) -> Direction:
        return self._direction

    @direction.setter
    def direction(self, value: Direction) -> None:
        if not isinstance(value, Direction):
            raise ValueError("Snake.direction has to be Direction type")
        
        # Do not change direction when new direction point into opposite direction
        if not (self.direction.value[0] + value.value[0] == 0 or self.direction.value[1] + value.value[1] == 0):
            self._direction = value


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

    def update(self) -> None:
        self.parts.append(PartInfo(((self.parts[-1].pos[0] + self.direction.value[0])%GRID_SIZE[0], (self.parts[-1].pos[1] + self.direction.value[1])%GRID_SIZE[1]), self.direction, self.direction))
        self.parts[-1].into = self.parts[-1].to
        if len(self.parts) >= 2:
            self.parts[-2].to = self.direction

        # Simulate snake growing by not deleting older parts for fix amunt of steps
        if self.pause <= 0:
            del self.parts[0]
        else:
            self.pause -= 1

    def draw(self) -> None:
        for index, part in enumerate(self.parts):
            if index == len(self.parts) - 1:
                pos = translate_idx2pos(part.pos, centered = False)
                display.blit(pygame.transform.rotate(Snake.head_image, self.direction.value[2] * 90), pos)
                #pos = translate_idx2pos(part.pos)
                #pygame.draw.circle(display, Color.GREEN, pos, min(CELL_SIZE)//2, 0)
            elif index == 0:
                pos = translate_idx2pos(part.pos)
                match part.to:
                    case Direction.EAST:
                        pygame.draw.rect(display, Color.GREEN, (pos[0] - CELL_SIZE[0]//4, pos[1] - CELL_SIZE[1]//4, CELL_SIZE[0]//4*3-1, CELL_SIZE[1]//2), 0)
                    case Direction.SOUTH:
                        pygame.draw.rect(display, Color.GREEN, (pos[0] - CELL_SIZE[0]//4, pos[1] - CELL_SIZE[1]//4, CELL_SIZE[0]//2, CELL_SIZE[1]//4*3-1), 0)
                    case Direction.WEST:
                        pygame.draw.rect(display, Color.GREEN, (pos[0] - CELL_SIZE[0]//2 + 1, pos[1] - CELL_SIZE[1]//4, CELL_SIZE[0]//4*3-1, CELL_SIZE[1]//2), 0)
                    case Direction.NORTH:
                        pygame.draw.rect(display, Color.GREEN, (pos[0] - CELL_SIZE[0]//4, pos[1] - CELL_SIZE[1]//2 + 1, CELL_SIZE[0]//2, CELL_SIZE[1]//4*3-1), 0)
            else:
                self._draw_part(part)
   

    def _draw_part(self, part: PartInfo) -> None:
        pos = translate_idx2pos(part.pos)
        
        if part.into == part.to:
            if part.into.value[0] == 0:
                pygame.draw.rect(display, Color.GREEN, (pos[0]-CELL_SIZE[0]//2 + 1, pos[1]-CELL_SIZE[1]//4, CELL_SIZE[0] - 2, CELL_SIZE[1]//2), 0)
            else:
                pygame.draw.rect(display, Color.GREEN, (pos[0]-CELL_SIZE[0]//4, pos[1]-CELL_SIZE[1]//2 + 1, CELL_SIZE[0]//2, CELL_SIZE[1] - 2), 0)
            return

        # works for clockwise
        match (part.into, part.to):
            case (Direction.SOUTH, Direction.EAST):
                rect_a = (pos[0] - CELL_SIZE[0]//4, pos[1] - CELL_SIZE[1]//4, CELL_SIZE[0]//4*3-1, CELL_SIZE[1]//2)
                rect_b = (pos[0] - CELL_SIZE[0]//4, pos[1] - CELL_SIZE[1]//2+1, CELL_SIZE[0]//2, CELL_SIZE[1]//4*3-1)

            case (Direction.SOUTH, Direction.WEST):
                rect_a = (pos[0] - CELL_SIZE[0]//2+1, pos[1] - CELL_SIZE[1]//4, CELL_SIZE[0]//4*3-1, CELL_SIZE[1]//2)
                rect_b = (pos[0] - CELL_SIZE[0]//4, pos[1] - CELL_SIZE[1]//2+1, CELL_SIZE[0]//2, CELL_SIZE[1]//4*3-1)

            case (Direction.NORTH, Direction.EAST):
                rect_a = (pos[0] - CELL_SIZE[0]//4, pos[1] - CELL_SIZE[1]//4, CELL_SIZE[0]//4*3-1, CELL_SIZE[1]//2)
                rect_b = (pos[0] - CELL_SIZE[0]//4, pos[1] - CELL_SIZE[1]//4, CELL_SIZE[0]//2, CELL_SIZE[1]//4*3-1)

            case (Direction.NORTH, Direction.WEST):
                rect_a = (pos[0] - CELL_SIZE[0]//2+1, pos[1] - CELL_SIZE[1]//4, CELL_SIZE[0]//4*3-1, CELL_SIZE[1]//2)
                rect_b = (pos[0] - CELL_SIZE[0]//4, pos[1] - CELL_SIZE[1]//4, CELL_SIZE[0]//2, CELL_SIZE[1]//4*3-1)

            case (Direction.EAST, Direction.NORTH):
                rect_a = (pos[0] - CELL_SIZE[0]//2+1, pos[1] - CELL_SIZE[1]//4, CELL_SIZE[0]//4*3-1, CELL_SIZE[1]//2)
                rect_b = (pos[0] - CELL_SIZE[0]//4, pos[1] - CELL_SIZE[1]//2+1, CELL_SIZE[0]//2, CELL_SIZE[1]//4*3-1)
            
            case (Direction.EAST, Direction.SOUTH):
                rect_a = (pos[0] - CELL_SIZE[0]//2+1, pos[1] - CELL_SIZE[1]//4, CELL_SIZE[0]//4*3-1, CELL_SIZE[1]//2)
                rect_b = (pos[0] - CELL_SIZE[0]//4, pos[1] - CELL_SIZE[1]//4, CELL_SIZE[0]//2, CELL_SIZE[1]//4*3-1)
            
            case (Direction.WEST, Direction.NORTH):
                rect_a = (pos[0] - CELL_SIZE[0]//4, pos[1] - CELL_SIZE[1]//4, CELL_SIZE[0]//4*3-1, CELL_SIZE[1]//2)
                rect_b = (pos[0] - CELL_SIZE[0]//4, pos[1] - CELL_SIZE[1]//2+1, CELL_SIZE[0]//2, CELL_SIZE[1]//4*3-1)
            
            case (Direction.WEST, Direction.SOUTH):
                rect_a = (pos[0] - CELL_SIZE[0]//4, pos[1] - CELL_SIZE[1]//4, CELL_SIZE[0]//4*3-1, CELL_SIZE[1]//2)
                rect_b = (pos[0] - CELL_SIZE[0]//4, pos[1] - CELL_SIZE[1]//4, CELL_SIZE[0]//2, CELL_SIZE[1]//4*3-1)

        pygame.draw.rect(display, Color.GREEN, rect_a, 0)
        pygame.draw.rect(display, Color.GREEN, rect_b, 0)


class DefaultSnake(Snake):
    """
    """
    def __init__(self):
        super().__init__([PartInfo((GRID_SIZE[0]//2, 2), Direction.EAST, Direction.EAST), PartInfo((GRID_SIZE[0]//2, 3), Direction.EAST, Direction.EAST)])
