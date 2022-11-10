import ast

from omok.game import Game
from omok.enums import TurnStateEnum
from tests import TestAgent
from tests.exc import TestEndError


def run_test(test_name, resource_manager):
    black_agent = TestAgent(
        TurnStateEnum.BLACK,
        resource_manager.read_text(f"/test_forbidden/black/{test_name}.txt")
    )
    white_agent = TestAgent(
        TurnStateEnum.WHITE,
        resource_manager.read_text(f"/test_forbidden/white/{test_name}.txt")
    )
    game = Game(
        black_agent=black_agent,
        white_agent=white_agent,
    )
    try:
        game.start()
    except TestEndError:
        pass
    assert set(game.rule.forbidden_points) == set(ast.literal_eval(
        resource_manager.read_text(
            f"/test_forbidden/forbidden/{test_name}.txt"
        )
    ))


def test_double_three_1(resource_manager):
    run_test("double_three_1", resource_manager)


def test_double_three_2(resource_manager):
    run_test("double_three_2", resource_manager)


def test_double_three_3(resource_manager):
    run_test("double_three_3", resource_manager)


def test_double_three_4(resource_manager):
    run_test("double_three_4", resource_manager)


def test_double_three_5(resource_manager):
    run_test("double_three_5", resource_manager)


def test_double_three_6(resource_manager):
    run_test("double_three_6", resource_manager)


def test_double_three_7(resource_manager):
    run_test("double_three_7", resource_manager)


def test_double_three_8(resource_manager):
    run_test("double_three_8", resource_manager)


def test_double_four_1(resource_manager):
    run_test("double_four_1", resource_manager)


def test_double_four_2(resource_manager):
    run_test("double_four_2", resource_manager)


def test_double_four_3(resource_manager):
    run_test("double_four_3", resource_manager)


def test_double_four_4(resource_manager):
    run_test("double_four_4", resource_manager)


def test_double_four_5(resource_manager):
    run_test("double_four_5", resource_manager)


def test_double_four_6(resource_manager):
    run_test("double_four_6", resource_manager)