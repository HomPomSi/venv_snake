#
#
#


import enum


class Direction(enum.Enum):
    "Position changes are index based"
    NORTH = (-1, 0, 3)
    EAST = (0, 1, 0)
    SOUTH = (1, 0, 1)
    WEST = (0, -1, 2)

