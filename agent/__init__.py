from game.enum import TurnStateEnum

class BaseAgent(object):
    """
    Base class for Agent

    """
    def __init__(self, turn: TurnStateEnum):
        self.turn = turn

    def get_next_point(self):
        raise NotImplementedError(
            "get_next_point() has to be implemented by subclasses"
        )
