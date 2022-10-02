from agent.base import BaseAgent
from enums import PointStateEnum, TurnStateEnum


class AlgorithmAgent(object):
    """
    Algorithm Agent

    """
    def __init__(self, turn: TurnStateEnum):
        super().__init__(turn)

    def move(self, board):
        row, col = self.get_point()
        return (row, col)

    def get_point(board):
        pass
