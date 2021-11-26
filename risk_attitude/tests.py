from otree.api import Bot, expect

from . import InfoSheet, Consent, Introduction, LotteryInstructions, LotteryUnderstanding, LotteryUnderstood, LotteryDecision


class PlayerBot(Bot):
    def play_round(self):
        expect("Macaulay Development Trust", "in", self.html)
        yield InfoSheet
        expect("I agree to take part in the experimental session.", "in", self.html)
        yield Consent, {"consent": True}
        expect(
            "You will receive £5.00 to thank you for your participation today.",
            "in",
            self.html,
        )
        expect(
            "into GBP at a rate of £1.00 per every 10 points.",
            "in",
            self.html,
        )
        yield Introduction
        yield LotteryInstructions
        yield LotteryUnderstanding, {"lottery_understanding": 32}
        expect(" 32 points. ", "in", self.html)
        yield LotteryUnderstood
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
        threshold = self.player.id % 11  # i.e. 0, 1, ..., 10 inclusive
        yield LotteryDecision, {f"lottery{i+1}": (i < threshold) for i in range(10)}

        expect(self.participant.payoff, self.player.payoff)  # first game/app
        lottery_selected = self.player.lottery_selected
        lottery_red = self.player.lottery_red
        expect(lottery_selected, ">=", 1)
        expect(lottery_selected, "<=", 10)

        if threshold < lottery_selected:
            # B was picked
            expect(self.player.payoff, 77 if lottery_red else 2)
        else:
            # A was picked
            expect(self.player.payoff, 40 if lottery_red else 32)
