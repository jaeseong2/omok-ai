import ast

import pytest

from omok.game import Game
from omok.enums import TurnStateEnum, GameStateEnum
from tests import TestAgent
from tests.exc import TestEndError

def run_test(test_name, resource_manager):
    black_agent = TestAgent(
        TurnStateEnum.BLACK,
        resource_manager.read_text(f"/test_five/black/{test_name}.txt")
    )
    white_agent = TestAgent(
        TurnStateEnum.WHITE,
        resource_manager.read_text(f"/test_five/white/{test_name}.txt")
    )
    game = Game(
        black_agent=black_agent,
        white_agent=white_agent,
    )
    try:
        game.start()
    except TestEndError:
        pass
    assert game.state == GameStateEnum.BLACK


def test_end_1(resource_manager):
    run_test("test_end_1", resource_manager)
