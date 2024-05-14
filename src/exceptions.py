#
#
#

class GameOverException(Exception):
    """Exception for when game enters invalid state at any point"""
    def __init__(self, msg: str) -> None:
        super().__init__(msg)

