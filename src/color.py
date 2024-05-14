#
#
#

from typing import Tuple

hextable = {"a": 10, "b": 11, "c": 12, "d": 13, "e": 14, "f": 15}

class BaseColor():
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    
    @staticmethod
    def hex2tuple(color: int) -> Tuple[int]:
        "actually works for any number type but hex is commenly used"
        return ((num//256**2)%256, (num//256)%256, num%256)


class Color(BaseColor):
    BACKGROUND = 0x222222
    GRID = 0x333333


