import copy

from omok.enums import TurnStateEnum, PointStateEnum
from omok.rule import Rule
from omok.config import BOARD_SIZE


class ScoringRule(Rule):
    def __init__(self):
        super(ScoringRule, self).__init__()
        self.score = 0

        self.score_info = {
            'six': 200 / 6,
            'five': 200 / 5,
            'double_open_four': 180,
            'open_four-open_three': 160,
            'open_four': 150 / 4,
            'four-open_three': 130,
            'double_open_three': 90,
            'four-three': 80,
            'open_three-open_two': 42,
            'double_open_two': 10,
            'four': 20 / 4,
            'open_three': 40 / 3,
            'three': 6 / 3,
            'open_two': 4 / 2,
            'two': 3 / 2
        }
        self.black_dict = {
            'five': [],
            'open_four-open_three': [],
            'open_four': [],
            'four-open_three': [],
            'four-three': [],
            'open_three-open_two': [],
            'double_open_two': [],
            'four': [],
            'open_three': [],
            'three': [],
            'open_two': [],
            'two': [],
        }
        self.white_dict = copy.deepcopy(self.black_dict)
        self.white_dict.update({
            'six': [],
            'double_open_four': [],
            'double_open_three': [],
        })

    def calculate_score(self, row, col, turn: TurnStateEnum, update=False):
        # calculate score when pointing at (row, col)
        start_row, end_row = max(0, row - 6), min(BOARD_SIZE, row + 6)
        start_col, end_col = max(0, col - 6), min(BOARD_SIZE, col + 6)
        previous_state = self.array[row][col]
        self.set_point_state(row, col, turn.point)
        for _row in range(start_row, end_row):
            for _col in range(start_col, end_col):
                self.calculate_point_score(_row, _col, turn, update)
        self.set_point_state(row, col, previous_state)

    def update_score(self, row, col, turn: TurnStateEnum, score = None):
        self.set_point_state(row, col, turn.point)
        if score is None:
            score = self.calculate_score(row, col, turn, True)
        self.score = score

    def calculate_point_score(self, row, col, turn, update):
        if turn == TurnStateEnum.BLACK and (row, col) in self.forbidden_points:
            return 0
        types, score = [], 0
        for directions in self.direction_sets:
            if self.check_open_three(row, col, turn.point, directions):
                types.append('open_three')
                continue
            if self.check_three(row, col, turn.point, directions):
                types.append('three')
                continue
            if self.check_open_four(row, col, turn.point, directions, True):
                types.append('open_four')
                continue
            if self.check_four(row, col, turn.point, directions):
                types.append('four')
                continue
            if self.check_five(row, col, turn.point, directions):
                types.append('five')
                continue
            if self.check_six(row, col, turn.point, directions):
                types.append('six')
                continue
        
