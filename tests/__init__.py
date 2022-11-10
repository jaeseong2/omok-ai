import ast

from omok.enums import TurnStateEnum
from agent import BaseAgent
from tests.exc import TestEndError


class TestAgent(BaseAgent):
    """
    Agent for test

    """
    def __init__(self, turn: TurnStateEnum, resource: str):
        self.points = ast.literal_eval(resource)
        self.index = 0

    def move(self, board):
        if self.index >= len(self.points):
            raise TestEndError
        points = self.points[self.index]
        self.index += 1
        return points
