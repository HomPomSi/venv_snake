#
#
#


from src import *
from src.utils import translate_idx2pos, translate_pos2idx
from src.exceptions import GameOverException
from typing import Tuple, List

class Consumable(object):
    "POSITIONS are handles as index"
    def __init__(self, pos: Tuple[int], lifetime: int = 15) -> None:
        self.pos = pos
        self.birth = time.time()
        self.lifetime = lifetime
        self.death = self.birth + self.lifetime
        self.is_alive = True

    def update(self) -> None:
        if time.time() >= self.death:
            self.is_alive = False

    def _consume(self) -> int:
        warnings.warn("Consumeable.consume() has not been implemented, consumable will not have any effects")
        return 0

    def consume(self) -> int:
        if self.is_alive:
            return self.value
        return 0

    def _draw(self) -> None:
        warnings.warn("Consumeable.draw() has not been implemented, consumable will not be drawn")

    def draw(self) -> None:
        if self.is_alive:
            self._draw()



class Fruit(Consumable):
    def __init__(self, pos: Tuple[int], image) -> None:
        super().__init__(pos)
        self.image = image
        self.value = 1

    def _draw(self) -> None:
        pos = translate_idx2pos(self.pos)
        display.blit(self.image, (pos[0] - 16, pos[1] - 16))



class Apple(Fruit):
    image = pygame.image.load("resources/apple.png")
    def __init__(self, pos: Tuple[int]) -> None:
        super().__init__(pos, Apple.image)
        self.value = 2

class Cherry(Fruit):
    image = pygame.image.load("resources/cherry.png")
    def __init__(self, pos: Tuple[int]) -> None:
        super().__init__(pos, Cherry.image)
        self.value = 1

class Ginger(Fruit):
    image = pygame.image.load("resources/ginger.png")
    def __init__(self, pos: Tuple[int]) -> None:
        super().__init__(pos, Ginger.image)
        self.value = -1

