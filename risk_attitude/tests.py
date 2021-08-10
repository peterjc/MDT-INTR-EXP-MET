from otree.api import Bot

from . import Introduction, LotteryInstructions, LotteryDecision


class PlayerBot(Bot):
    def play_round(self):
        yield Introduction
        yield LotteryInstructions
        # Risk averse people should always pick A, risk taking ones B,
        # and there should be a switching point to B for everyone.
        #
        # Code will submit the following:
        # threshold 0 - none True, all False. Risk taking
        #               i.e. B, B, B, B, ..., B
        # threshold 1 - one True, nine False.
        #               i.e. A, B, B, ..., B, B
        # ...
        # threshold 9 - nine True, one False. Risk averse
        #               i.e. A, A, A, ..., A, B
        # threshold 10 - all True. Risk averse + wrong on last round
        #                i.e. A, A, A, ..., A
        #
        # Player ID seems to be an autoincrement linked to past DB usage, so
        # if tests run with just 6 players only a subset of thresholds used!
        threshold = (self.player.id % 11)  # i.e. 0, 1, ..., 10 inclusive
        yield LotteryDecision, {f"lottery{i+1}": (i >= threshold) for i in range(10)}
