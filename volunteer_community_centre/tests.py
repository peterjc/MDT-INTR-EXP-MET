from otree.api import Bot

from . import Instructions, Volunteering, Results


class PlayerBot(Bot):
    def play_round(self):
        if self.round_number == 1:
            yield Instructions
        # yield WaitToStart <-- automatic
        yield Volunteering, {"volunteer": False}
        yield Results
