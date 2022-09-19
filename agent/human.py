from agent import BaseAgent
from game.exc import CanNotSelectError

class HumanAgent(BaseAgent):
    """
    Agent for human
    Get input from std

    """
    def __init__(self, turn):
        super().__init__(turn)

    def get_next_point(self, array, possibles):
        row, col = input("Input(row, col): ").split()
        row, col = int(row), int(col)
        if (row, col) not in possibles:
            raise CanNotSelectError
        return (row, col)
