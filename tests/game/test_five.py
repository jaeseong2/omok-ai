import ast

import pytest

from game import Game
from enums import GameMode, TurnStateEnum
from game.exc import GameEndError
from tests import TestAgent


def run_test(test_name, resource_manager, winner):
    black_agent = TestAgent(
        resource_manager.read_text(f"/test_five/black/{test_name}.txt")
    )
    white_agent = TestAgent(
        resource_manager.read_text(f"/test_five/white/{test_name}.txt")
    )
    game_board = Game(
        black_agent=black_agent,
        white_agent=white_agent,
    )
    with pytest.raises(GameEndError) as e:
        game_board.start()


def test_end_1(resource_manager):
    run_test("test_end_1", resource_manager, TurnStateEnum.BLACK)
