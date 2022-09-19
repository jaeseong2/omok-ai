import enum

class GameMode(enum.Enum):
    HUMAN_HUMAN = "HUMAN_HUMAN"
    HUMAN_COMPUTER = "HUMAN_COMPUTER"
    COMPUTER_HUMAN = "COMPUTER_HUMAN"
    COMPUTER_COMPUTER = "COMPUTER_COMPUTER"
    TEST = "TEST"


class PointStateEnum(enum.Enum):
    EMPTY = 0
    UNSELECTABLE = 1
    BLACK = 2
    WHITE = 3

    def get_opposite(self):
        if self == self.BLACK:
            return self.WHITE
        elif self == self.WHITE:
            return self.BLACK
        else:
            raise ValueError(
                f'{self.value} has no opposite'
            )


class TurnStateEnum(enum.Enum):
    BLACK = 0
    WHITE = 1

    def get_opposite(self):
        if self == self.BLACK:
            return self.WHITE
        else:
            return self.BLACK


class GamestateEnum(enum.Enum):
    CONTINUE = 0
    BLACK = 1
    WHITE = 2
    DRAW = 3
