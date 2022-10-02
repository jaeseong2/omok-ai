from enums import TurnStateEnum

class BaseAgent(object):
    """
    Base class for Agent

    """
    def __init__(self, turn: TurnStateEnum):
        self.turn = turn

    def move(self):
        raise NotImplementedError(
            "move() has to be implemented by subclasses"
        )
