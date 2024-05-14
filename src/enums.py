#
#
#


import enum


class Direction(enum.Enum):
    """
    Position changes are index based.
    value resembels (ROW_DELTA, COLUMN_DELTA, N * 90° clockwise rotation, starting with 0 degrees at EAST)
    """
    NORTH = (-1, 0, 3)
    EAST = (0, 1, 0)
    SOUTH = (1, 0, 1)
    WEST = (0, -1, 2)

