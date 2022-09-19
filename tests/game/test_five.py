import ast

import pytest

from game.board import GameBoard
from game.enum import GameMode, TurnStateEnum
from game.exc import GameEndError
from tests import TestAgent


def run_test(test_name, resource_manager, winner):
    black_agent = TestAgent(
        resource_manager.read_text(f"/test_five/black/{test_name}.txt")
    )
    white_agent = TestAgent(
        resource_manager.read_text(f"/test_five/white/{test_name}.txt")
    )
    game_board = GameBoard(
        black_agent=black_agent,
        white_agent=white_agent,
    )
    with pytest.raises(GameEndError) as e:
        game_board.start()
    assert str(e.value) == str(winner)


def test_end_1(resource_manager):
    run_test("test_end_1", resource_manager, TurnStateEnum.BLACK)
