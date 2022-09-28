from .enum import GameMode, PointStateEnum, TurnStateEnum, GameStateEnum
from .exc import (
    OutOfIndexError,
    CanNotSelectError,
    GameEndError,
    TestEndError,
)
from .config import BOARD_SIZE


class Game(object):
    """
    Game class for omok
    Contain enviroment information for game

    """

    def __init__(self, black_agent, white_agent):
        self.initialize()
        self.board_size = BOARD_SIZE
        self.black_agent = black_agent
        self.white_agent = white_agent
        self.directions = [
            [(1, 0), (-1, 0)],
            [(0, 1), (0, -1)],
            [(1, 1), (-1, -1)],
            [(1, -1), (-1, 1)],
        ]

        try:
            self.move_functions = [
                self.black_agent.get_next_point,
                self.white_agent.get_next_point
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
            ]) for line in self.board
        ])

    def initialize(self):
        self.board = list()
        self.empty_points = list()
        for i in range(BOARD_SIZE):
            line = list()
            for j in range(BOARD_SIZE):
                line.append(PointStateEnum.EMPTY)
                self.empty_points.append((i, j))
            self.board.append(line)

        self.forbidden_points = list()
        self.turn = TurnStateEnum.BLACK
        self.total_empty_count = BOARD_SIZE * BOARD_SIZE

    def change_turn(self):
        if self.turn == TurnStateEnum.BLACK:
            self.turn = TurnStateEnum.WHITE
        else:
            self.turn = TurnStateEnum.BLACK

    def get_current_point_state(self):
        state_map = {
            TurnStateEnum.BLACK: PointStateEnum.BLACK,
            TurnStateEnum.WHITE: PointStateEnum.WHITE
        }
        return state_map[self.turn]

    def is_out_of_board(self, point):
        row, col = point
        return (
            row < 0 or BOARD_SIZE - 1 < row
            or col < 0 or BOARD_SIZE - 1 < col
        )

    def set_point_state(self, point, state: PointStateEnum):
        row, col = point
        self.board[row][col] = state

    def get_state_count(self, point, state: PointStateEnum, direction):
        '''
        Get count of points same with given state
        The count includes start point
        '''
        row, col = point
        cnt = 1
        while True:
            row, col = row + direction[0], col + direction[1]
            if self.is_out_of_board(row, col) or self.board[row][col] != state:
                break
            else:
                cnt += 1
        return cnt

    def find_empty_point(self, point, state: PointStateEnum, direction):
        row, col = point
        while True:
            row, col = row + direction[0], col + direction[1]
            if self.is_out_of_board(row, col) or self.board[row][col] == state.opposite:
                return None
            if self.board[row][col] == PointStateEnum.EMPTY:
                return row, col

    def check_open_three(self, point, state, direction):
        row, col = point
        for i in range(2):
            coord = self.find_empty_point(row, col, state, direction * 2 + i)
            if coord:
                dx, dy = coord
                self.set_point_state(dx, dy, state)
                if 1 == self.open_four(dx, dy, state, direction):
                    if not self.forbidden_point(dx, dy, state):
                        self.set_point_state(dx, dy, empty)
                        return True
                self.set_point_state(dx, dy, empty)
        return False

    def check_open_four(self, point, state, direction):
        row, col =point
        if self.is_five(x, y, state):
            return False
        cnt = 0
        for i in range(2):
            coord = self.find_empty_point(x, y, state, direction * 2 + i)
            if coord:
                if self.check_five(coord[0], coord[1], state, direction):
                    cnt += 1
        if cnt == 2:
            if 4 == self.get_state_count(x, y, state, direction):
                cnt = 1
        else: cnt = 0
        return cnt

    def check_four(self, point, state, direction):
        row, col = point
        for i in range(2):
            coord = self.find_empty_point(x, y, state, direction * 2 + i)
            if coord:
                if self.check_five(coord[0], coord[1], state, direction):
                    return True
        return False


    def check_five(self, point, state, direction):
        if self.get_state_count(self, point, state, direction) == 5:
            return True
        return False

    def check_six(self, point, state, direction):
        if self.get_state_count(self, point, state, direction) > 5:
            return True
        return False

    def check_double_three(self, point, state):
        cnt = 0
        row, col = point
        self.set_point_state(row, col, state)
        for i in range(4):
            if self.open_three(row, col, state, i):
                cnt += 1
        self.set_point_state(row, col, empty)
        if cnt >= 2:
            # print("double three")
            return True
        return False

    def check_double_four(self, point, state):

        cnt = 0
        self.set_point_state(x, y, state)
        for i in range(4):
            if self.open_four(x, y, state, i) == 2:
                cnt += 2
            elif self.four(x, y, state, i):
                cnt += 1
        self.set_point_state(x, y, empty)
        if cnt >= 2:
            # print("double four")
            return True
        return False


    def set_forbidden_points(self, point):
        row, col = point
        start_row, end_row = max(0, row - 5), min(BOARD_SIZE, row + 5)
        start_col, end_col = max(0, col - 5), min(BOARD_SIZE, col + 5)

        for row in range(start_row, end_row):
            for col in range(start_col, end_col):
                if self.board[row][col] == PointStateEnum.EMPTY:
                    if self.check_forbidden((row, col)):
                        self.board[row][col] = PointStateEnum.FORBIDDEN
                        self.forbidden_points.append((row, col))

                if self.board[row][col] == PointStateEnum.FORBIDDEN:
                    if not self.check_forbidden((row, col)):
                        self.board[row][col] = PointStateEnum.EMPTY
                        self.forbidden_points.remove((row, col))


    def start(self):
        while True:
            try:
                for move_function in self.move_functions:
                    if self.turn == TurnStateEnum.BLACK:
                        possible = set(self.empty_points).difference(
                            set(self.forbidden_points)
                        )
                    else:
                        possible = set(self.empty_points)
                    row, col = move_function(self.board, possible)
                    point = (row, col)
                    self.set_point_state(
                        point,
                        self.get_current_point_state()
                    )
                    self.empty_points.remove(point)
                    self.total_empty_count -= 1

                    if self.turn == TurnStateEnum.BLACK:
                        self.check_finished(
                            self.total_empty_count - len(self.forbidden_points),
                            point
                        )
                        self.set_forbidden_points(point)
                    else:
                        self.check_finished(
                            self.total_empty_count,
                            point
                        )
                        if self.board[row][col] == PointStateEnum.FORBIDDEN:
                            self.forbidden_points.remove(point)
                        self.set_selectable_points()
                    self.change_turn()

            except KeyboardInterrupt:
                print("Stop Game by keyboard interrupt")
                break
            except TestEndError:
                break
