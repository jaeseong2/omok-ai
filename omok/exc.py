from omok.enums import TurnStateEnum

class OutOfIndexError(Exception):
    def __init__(self):
        super().__init__('Size of array is 15 x 15 (0 - 14)')


class CanNotSelectError(Exception):
    def __init__(self):
        super().__init__('Can not set in this position')


class TestEndError(Exception):
    pass

