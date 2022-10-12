from multiprocessing import Lock

from omok.enums import GameMode, PointStateEnum, TurnStateEnum, GameStateEnum
from omok.exc import (
    OutOfIndexError,
    CanNotSelectError,
    TestEndError,
)
from omok.config import BOARD_SIZE
from omok.rule import Rule
from agent import BaseAgent, HumanAgent


class Game(object):
    """
    Game class for omok
    Contain enviroment information for game

    """

    def __init__(self, black_agent: BaseAgent, white_agent: BaseAgent):
        self.initialize()
        self.board_size = BOARD_SIZE
        self.black_agent = black_agent
        self.white_agent = white_agent
        self.lock = Lock()
        self.rule = Rule()

        try:
            self.move_functions = [
                self.black_agent.move,
                self.white_agent.move
            ]
        except AttributeError:
            raise ValueError("Invalid agent")

    def __str__(self):
        str_map = {
            PointStateEnum.EMPTY: ".",
            PointStateEnum.FORBIDDEN: "X",
            PointStateEnum.BLACK: "B",
            PointStateEnum.WHITE: "W",
        }
        return "\n".join([
            " ".join([
                str_map[point] for point in line
            ]) for line in self.rule.array
        ])

    def initialize(self):
        self.forbidden_points = list()
        self.current_turn = TurnStateEnum.BLACK
        self.current_point_state = PointStateEnum.BLACK
        self.state = GameStateEnum.CONTINUE
        self.empty_point_count = BOARD_SIZE * BOARD_SIZE
        self.turn_ready = True

    def change_turn(self):
        if self.current_turn == TurnStateEnum.BLACK:
            self.current_turn = TurnStateEnum.WHITE
            self.current_point_state = PointStateEnum.WHITE
        else:
            self.current_turn = TurnStateEnum.BLACK
            self.current_point_state = PointStateEnum.BLACK

    def is_out_of_board(self, row, col):
        return (
            row < 0 or BOARD_SIZE - 1 < row
            or col < 0 or BOARD_SIZE - 1 < col
        )

    def check_game_state(self, row, col):
        if self.current_turn == TurnStateEnum.BLACK:
            if self.rule.check_five(row, col, PointStateEnum.BLACK):
                self.state = GameStateEnum.BLACK
                return True
            left = self.empty_point_count - len(self.forbidden_points)
        else:
            if self.rule.check_five(row, col, PointStateEnum.WHITE):
                self.state = GameStateEnum.WHITE
                return True
            left = self.empty_point_count
        if left == 0:
            self.state = GameStateEnum.DRAW
            return True
        return False

    def start(self):
        while True:
            try:
                if (
                    isinstance(self.black_agent, HumanAgent)
                    or isinstance(self.white_agent, HumanAgent)
                ):
                    self.lock.acquire()
                for agent in [self.black_agent, self.white_agent]:
                    if isinstance(agent, HumanAgent):
                        self.lock.release()
                    row, col = agent.move_function(self.rule.array)

                    if isinstance(agent, HumanAgent):
                        self.lock.acquire()
                    self.set_point_state(row, col, self.current_point_state)
                    self.empty_point_count -= 1
                    if self.check_game_state(row, col):
                        self.lock.release()
                        return
                    if self.current_turn == TurnStateEnum.BLACK:
                        self.rule.set_forbidden_points(row, col)
                    else:
                        if self.rule.array[row][col] == PointStateEnum.FORBIDDEN:
                            self.rule.forbidden_points.remove((row, col))
                    self.change_turn()

            except KeyboardInterrupt:
                break
            except TestEndError:
                break
