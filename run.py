import click

from game import Game
from enums import GameMode, TurnStateEnum
from agent.human import HumanAgent
from agent.algorithm import AlgorithmAgent

@click.command()
@click.option('--mode', default='HUMAN_HUMAN', help='')
def run(mode):
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
    game = Game(black_agent, white_agent)
    game.start()


if __name__ == "__main__":
    run()
