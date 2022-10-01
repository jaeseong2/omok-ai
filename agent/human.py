from multiprocessing import Queue
import time

from agent import BaseAgent
from enums import PointStateEnum, TurnStateEnum


class HumanAgent(BaseAgent):
    """
    Agent for human
    Get input from pygame

    """
    def __init__(self, turn: TurnStateEnum):
        super().__init__(turn)
        self.input_queue = Queue()

    def move(self, board):
        row, col = self.input_queue.get()
        if self.turn == TurnStateEnum.BLACK:
            while board[row][col] == PointStateEnum.FORBIDDEN:
                time.sleep(0.1)
                row, col = self.input_queue.get()
        return (row, col)
