from omok.enums import GameMode, PointStateEnum, TurnStateEnum, GameStateEnum
from omok.config import BOARD_SIZE


class Rule(object):
    """
    Rule class for omok

    """
    def __init__(self):
        self.initialize()
        self.direction_sets = [
            [(1, 0), (-1, 0)],
            [(0, 1), (0, -1)],
            [(1, 1), (-1, -1)],
            [(1, -1), (-1, 1)],
        ]

    def initialize(self):
        self.array = list()
        for i in range(BOARD_SIZE):
            line = list()
            for j in range(BOARD_SIZE):
                line.append(PointStateEnum.EMPTY)
            self.array.append(line)

        self.forbidden_points = list()

    def is_out_of_board(self, row, col):
        return (
            row < 0 or BOARD_SIZE - 1 < row
            or col < 0 or BOARD_SIZE - 1 < col
        )

    def set_point_state(self, row, col, state: PointStateEnum):
        self.array[row][col] = state

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
                if self.is_out_of_board(_row, _col) or self.array[_row][_col] != state:
                    break
                else:
                    count += 1
        return count

    def get_row_state(self, row, col, state, directions):
        points = [(row, col)]
        blank_count = 0
        for direction in directions:
            _row, _col = row, col
            while True:
                _row, _col = _row + direction[0], _col + direction[1]
                if self.is_out_of_board(_row, _col):
                    break
                if self.array[_row][_col] == state:
                    points.append((_row, _col))
                elif self.array[_row][_col] == PointStateEnum.EMPTY:
                    if blank_count + len(points) > 5:
                        break
                    blank_count += 1
                else:
                    break
        return points, blank_count

    def get_direction_points_map(self, row, col, state, direction_sets = None):
        direction_points_dict = {}
        if direction_sets is None:
            direction_sets = self.direction_sets
        for i, directions in enumerate(direction_sets):
            points = self.get_row_state(row, col, state, directions)
            if len(points) > 1:
                direction_points_dict[i] = points
        return direction_points_dict

    def find_empty_point(self, row, col, state: PointStateEnum, direction):
        '''
        Find empty point at end of line
        '''
        while True:
            row, col = row + direction[0], col + direction[1]
            if self.is_out_of_board(row, col) or self.array[row][col] == state.opponent:
                return None
            if self.array[row][col] in [PointStateEnum.EMPTY, PointStateEnum.FORBIDDEN]:
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
                previous_state = self.array[empty_row][empty_col]
                self.set_point_state(empty_row, empty_col, state)
                if self.check_open_four(empty_row, empty_col, state, directions, True):
                    if row == 7 and col == 10:
                        print(empty_row, empty_col)
                    self.set_point_state(empty_row, empty_col, previous_state)
                    return True
                self.set_point_state(empty_row, empty_col, previous_state)
        return False

    def check_open_four(self, row, col, state, directions, seq=False):
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
                if seq:
                    count = 0
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
        previous_state = self.array[row][col]
        self.set_point_state(row, col, state)
        for directions in self.direction_sets:
            if self.check_open_three(row, col, state, directions):
                count += 1
        self.set_point_state(row, col, previous_state)
        if count >= 2:
            return True
        return False

    def check_double_four(self, row, col, state):
        '''
        Check given point is double three point
        
        '''
        count = 0
        previous_state = self.array[row][col]
        self.set_point_state(row, col, state)
        for directions in self.direction_sets:
            if self.check_open_four(row, col, state, directions) == 2:
                count += 2
            elif self.check_four(row, col, state, directions):
                count += 1
        self.set_point_state(row, col, previous_state)
        if count >= 2:
            return True
        return False

    def check_forbidden(self, row, col):
        if self.array[row][col] in [PointStateEnum.BLACK, PointStateEnum.WHITE]:
            return False
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

        # remove
        for row, col in self.forbidden_points:
            if not self.check_forbidden(row, col):
                self.array[row][col] = PointStateEnum.EMPTY
                self.forbidden_points.remove((row, col))

        # append new
        for row in range(start_row, end_row):
            for col in range(start_col, end_col):
                if self.array[row][col] == PointStateEnum.EMPTY:
                    if self.check_forbidden(row, col):
                        self.array[row][col] = PointStateEnum.FORBIDDEN
                        self.forbidden_points.append((row, col))
