import click

from omok.game import Game
from omok.enums import GameMode, TurnStateEnum
from agent.human import HumanAgent
from agent.algorithm import AlgorithmAgent
from omok.board import Board


@click.command()
@click.option('--mode', default='HUMAN_HUMAN', help='')
def run_game(mode):
    mode = GameMode(mode)
    if mode == GameMode.HUMAN_HUMAN:
        black_agent = HumanAgent(TurnStateEnum.BLACK)
        white_agent = HumanAgent(TurnStateEnum.WHITE)
    elif mode == GameMode.HUMAN_COMPUTER:
        black_agent = HumanAgent(TurnStateEnum.BLACK)
        white_agent = AlgorithmAgent(TurnStateEnum.WHITE)
    elif mode == GameMode.COMPUTER_HUMAN:
        black_agent = AlgorithmAgent(TurnStateEnum.BLACK)
        white_agent = HumanAgent(TurnStateEnum.WHITE)
    else:
        black_agent = AlgorithmAgent(TurnStateEnum.BLACK)
        white_agent = AlgorithmAgent(TurnStateEnum.WHITE)
    board = Board(black_agent, white_agent)
    board.start()
