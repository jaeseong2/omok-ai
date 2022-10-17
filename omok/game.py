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
        self.rule: Rule = Rule()

        try:
            self.move_functions = [
                self.black_agent.move,
                self.white_agent.move
            ]
        except AttributeError:
            raise ValueError("Invalid agent")

    def __str__(self):
        str_map = {
            PointStateEnum.EMPTY: ". ",
            PointStateEnum.FORBIDDEN: "X ",
            PointStateEnum.BLACK: "B ",
            PointStateEnum.WHITE: "W ",
        }
        index_rule = lambda x: str(x) + " " if len(str(x)) == 1 else str(x)
        return "\n".join(
            ["   " + " ".join(index_rule(x) for x in range(0, BOARD_SIZE))] +
            [
                " ".join([index_rule(y)] + [
                    str_map[point] for point in line
                ]) for y, line in enumerate(self.rule.array)
            ]
        )

    def initialize(self):
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

    def check_game_state(self, row, col):
        if self.current_turn == TurnStateEnum.BLACK:
            if self.rule.check_five(row, col, PointStateEnum.BLACK):
                self.state = GameStateEnum.BLACK
                return True
            left = self.empty_point_count - len(self.rule.forbidden_points)
        else:
            if (
                self.rule.check_five(row, col, PointStateEnum.WHITE)
                or self.rule.check_six(row, col, PointStateEnum.WHITE)
            ):
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
                    row, col = agent.move(self.rule.array)

                    if isinstance(agent, HumanAgent):
                        self.lock.acquire()
                    self.rule.set_point_state(row, col, self.current_point_state)
                    self.empty_point_count -= 1
                    if self.check_game_state(row, col):
                        if isinstance(agent, HumanAgent):
                            self.lock.acquire()
                        return
                    self.change_turn()
                    self.rule.set_forbidden_points(row, col)
                    print(self.rule.forbidden_points)

            except KeyboardInterrupt:
                break
            except TestEndError:
                break
