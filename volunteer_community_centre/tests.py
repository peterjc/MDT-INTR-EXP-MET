from otree.api import Bot, expect

from . import Instructions, Volunteering, Results


class PlayerBot(Bot):
    def play_round(self):
        if self.round_number == 1:
            yield Instructions
        # yield WaitToStart <-- automatic
        yield Volunteering, {"volunteer": False}
        expect("<p>Thanks for making your choice.</p>", "in", self.html)
        expect(
            "No one in your group volunteered. You earned 0 tokens.", "in", self.html
        )
        yield Results
