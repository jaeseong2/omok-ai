from enums import GameMode, PointStateEnum, TurnStateEnum, GameStateEnum
from .exc import (
    OutOfIndexError,
    CanNotSelectError,
    GameEndError,
    TestEndError,
)
from config import BOARD_SIZE


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
        self.direction_sets = [
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
        for i in range(BOARD_SIZE):
            line = list()
            for j in range(BOARD_SIZE):
                line.append(PointStateEnum.EMPTY)
            self.board.append(line)

        self.forbidden_points = list()
        self.current_turn = TurnStateEnum.BLACK
        self.current_point_state = PointStateEnum.BLACK
        self.game_state = GameStateEnum.CONTINUE
        self.empty_point_count = BOARD_SIZE * BOARD_SIZE

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

    def set_point_state(self, row, col, state: PointStateEnum):
        self.board[row][col] = state

    def get_state_count(self, row, col, state: PointStateEnum, directions):
        '''
        Get count of points same with given state
        The count includes start point
        '''
        count = 1
        for direction in directions:
            _row, _col = row, col
            while True:
                _row, _col = _row + direction[0], _col + direction[1]
                if self.is_out_of_board(_row, _col) or self.board[_row][_col] != state:
                    break
                else:
                    count += 1
        return count

    def find_empty_point(self, row, col, state: PointStateEnum, direction):
        '''
        Find empty point at end of line
        '''
        while True:
            row, col = row + direction[0], col + direction[1]
            if self.is_out_of_board(row, col) or self.board[row][col] == state.opposite:
                return None
            if self.board[row][col] == PointStateEnum.EMPTY:
                return row, col

    def check_open_three(self, row, col, state, directions):
        '''
        Find empty point and set the point as target state
        Then check the line is open four or not
        '''
        for direction in directions:
            empty_point = self.find_empty_point(row, col, state, direction)
            if empty_point:
                empty_row, empty_col = empty_point
                self.set_point_state(empty_row, empty_col, state)
                if (
                    self.check_open_four(empty_row, empty_col, state, directions)
                    and not self.check_forbidden(empty_row, empty_col)
                ):
                    self.set_point_state(empty_row, empty_col, PointStateEnum.EMPTY)
                    return True
                self.set_point_state(empty_row, empty_col, PointStateEnum.EMPTY)
        return False

    def check_open_four(self, row, col, state, directions):
        if self.check_five(row, col, state):
            return False
        count = 0
        for direction in directions:
            empty_point = self.find_empty_point(row, col, state, direction)
            if empty_point:
                empty_row, empty_col = empty_point
                if self.check_five(empty_row, empty_col, state, directions):
                    count += 1
        if count == 2:
            if self.get_state_count(row, col, state, directions) == 4:
                count = 1
        else:
            count = 0
        return count

    def check_four(self, row, col, state, directions):
        '''
        Check open and closed four
        '''
        for direction in directions:
            empty_point = self.find_empty_point(row, col, state, direction)
            if empty_point:
                if self.check_five(empty_point[0], empty_point[1], state, directions):
                    return True
        return False

    def check_five(self, row, col, state, directions=None):
        if directions is None:
            direction_sets = self.direction_sets
        else:
            direction_sets = [directions]

        for directions in direction_sets:
            if self.get_state_count(row, col, state, directions) == 5:
                return True
        return False

    def check_six(self, row, col, state, directions=None):
        if directions is None:
            direction_sets = self.direction_sets
        else:
            direction_sets = [directions]

        for directions in direction_sets:
            if self.get_state_count(row, col, state, directions) > 5:
                return True
        return False

    def check_double_three(self, row, col, state):
        '''
        Check given point is double three point in all directions
        '''
        count = 0
        self.set_point_state(row, col, state)
        for directions in self.direction_sets:
            if self.check_open_three(row, col, state, directions):
                count += 1
        self.set_point_state(row, col, PointStateEnum.EMPTY)
        if count >= 2:
            return True
        return False

    def check_double_four(self, row, col, state):
        '''
        Check given point is double three point
        
        '''
        count = 0
        self.set_point_state(row, col, state)
        for directions in self.direction_sets:
            if self.check_open_four(row, col, state, directions) == 2:
                count += 2
            elif self.check_four(row, col, state, directions):
                count += 1
        self.set_point_state(row, col, PointStateEnum.EMPTY)
        if count >= 2:
            return True
        return False

    def check_forbidden(self, row, col):
        if self.check_five(row, col, PointStateEnum.BLACK):
            return False
        elif self.check_six(row, col, PointStateEnum.BLACK):
            return True
        elif (
            self.check_double_three(row, col, PointStateEnum.BLACK)
            or self.check_double_four(row, col, PointStateEnum.BLACK)
        ):
            return True
        return False

    def set_forbidden_points(self, row, col):
        start_row, end_row = max(0, row - 5), min(BOARD_SIZE, row + 5)
        start_col, end_col = max(0, col - 5), min(BOARD_SIZE, col + 5)

        for row in range(start_row, end_row):
            for col in range(start_col, end_col):
                if self.board[row][col] == PointStateEnum.EMPTY:
                    if self.check_forbidden(row, col):
                        self.board[row][col] = PointStateEnum.FORBIDDEN
                        self.forbidden_points.append((row, col))
                elif self.board[row][col] == PointStateEnum.FORBIDDEN:
                    if not self.check_forbidden(row, col):
                        self.board[row][col] = PointStateEnum.EMPTY
                        self.forbidden_points.remove((row, col))

    def check_finished(self, row, col):
        if self.current_turn == TurnStateEnum.BLACK:
            if self.check_five(row, col, PointStateEnum.BLACK):
                self.game_state = GameStateEnum.BLACK
                return True
            left = self.empty_point_count - len(self.forbidden_points)
        else:
            if self.check_five(row, col, PointStateEnum.WHITE):
                self.game_state = GameStateEnum.WHITE
                return True
            left = self.empty_point_count
        if left == 0:
            self.game_state = GameStateEnum.DRAW
            return True
        return False

    def start(self):
        while True:
            try:
                for move_function in self.move_functions:
                    row, col = move_function(self.board)
                    self.set_point_state(row, col, self.current_point_state)
                    self.empty_point_count -= 1
                    if self.check_finished(row, col):
                        print('Finished')
                        raise GameEndError
                    if self.current_turn == TurnStateEnum.BLACK:
                        self.set_forbidden_points(row, col)
                    else:
                        if self.board[row][col] == PointStateEnum.FORBIDDEN:
                            self.forbidden_points.remove((row, col))
                    self.change_turn()

            except KeyboardInterrupt:
                break
            except TestEndError:
                break
