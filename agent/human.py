from agent import BaseAgent
from game.exc import CanNotSelectError
from enums import PointStateEnum

class HumanAgent(BaseAgent):
    """
    Agent for human
    Get input from std

    """
    def __init__(self, turn):
        super().__init__(turn)

    def get_next_point(self, board):
        row, col = input("Input(row, col): ").split()
        row, col = int(row), int(col)
        if board[row][col] == PointStateEnum.FORBIDDEN:
            raise CanNotSelectError
        return (row, col)
