import ast

import pytest

from agent.scoring_rule import ScoringRule
from omok.enums import TurnStateEnum
from tests import TestAgent
from tests.exc import TestEndError


def run_test(test_name, resource_manager):
    black_agent = TestAgent(
        TurnStateEnum.BLACK,
        resource_manager.read_text(f"/black/{test_name}.txt")
    )
    white_agent = TestAgent(
        TurnStateEnum.WHITE,
        resource_manager.read_text(f"/white/{test_name}.txt")
    )
    target_scores = ast.literal_eval(
        resource_manager.read_text(f"/scores/{test_name}.txt")
    )

    scoring_rule = ScoringRule()
    for i in range(len(black_agent.points)):
        row, col = black_agent.move(scoring_rule.array)
        scoring_rule.update_score(row, col, black_agent.turn)
        row, col = white_agent.move(scoring_rule.array)
        scoring_rule.update_score(row, col, white_agent.turn)

        assert scoring_rule.score == target_scores[i]


def test_calculate_score_1(resource_manager):
    run_test("1", resource_manager)
