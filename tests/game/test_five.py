import ast

import pytest

from game import Game
from omok.enums import TurnStateEnum, GameStateEnum
from tests import TestAgent


def run_test(test_name, resource_manager, winner):
    black_agent = TestAgent(
        resource_manager.read_text(f"/test_five/black/{test_name}.txt")
    )
    white_agent = TestAgent(
        resource_manager.read_text(f"/test_five/white/{test_name}.txt")
    )
    game = Game(
        black_agent=black_agent,
        white_agent=white_agent,
    )
    game.start()
    assert game.state == GameStateEnum.BLACK


def test_end_1(resource_manager):
    run_test("test_end_1", resource_manager, TurnStateEnum.BLACK)
