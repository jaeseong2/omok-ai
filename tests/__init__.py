import ast

from agent import BaseAgent
from game.exc import TestEndError

class TestAgent(BaseAgent):
    """
    Agent for test

    """
    def __init__(self, resource: str):
        self.points = ast.literal_eval(resource)
        self.index = 0

    def get_next_point(self, array, possibles):
        if self.index >= len(self.points):
            raise TestEndError
        points = self.points[self.index]
        self.index += 1
        return points
