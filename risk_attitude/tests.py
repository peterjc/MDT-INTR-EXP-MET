from otree.api import Bot

from . import Introduction, LotteryInstructions, LotteryDecision


class PlayerBot(Bot):
    def play_round(self):
        yield Introduction
        yield LotteryInstructions
        yield LotteryDecision, {f"lottery{i+1}": True for i in range(10)}
