from otree.api import Bot, expect

from . import Instructions, Volunteering, Results


class PlayerBot(Bot):

    cases = ["never", "all"]

    def play_round(self):
        if self.round_number == 1:
            yield Instructions
        # yield WaitToStart <-- automatic
        if self.case == "never":
            # Do with timeout?
            yield Volunteering, {"volunteer": False}
            expect("<p>Thanks for making your choice.</p>", "in", self.html)
            expect(
                "No one in your group volunteered. You earned 0 tokens.",
                "in",
                self.html,
            )
            expect(self.player.payoff, 0)
        else:
            yield Volunteering, {"volunteer": True}
            expect("<p>Thanks for making your choice.</p>", "in", self.html)
            if self.player.id_in_group == 1:
                # Appears bot for player one is always first
                expect("You volunteered first.", "in", self.html)
                if self.round_number in [1, 2, 5]:
                    expect(self.player.payoff, 0)  # self-less
                else:
                    expect(self.player.payoff, 50)  # compensated
                if self.round_number == 5:
                    # Game over, 0 + 0 + 50 + 50 + 0
                    expect(self.participant.payoff, 100)
            else:
                expect(
                    "Another person in your group volunteered first.", "in", self.html
                )
                if self.round_number in [1, 2, 5]:
                    expect(self.player.payoff, 50)  # free-loader
                else:
                    expect(self.player.payoff, 40)  # compensation deduction
                if self.round_number == 5:
                    # Game over, 50 + 50 + 40 + 40 + 50
                    expect(self.participant.payoff, 230)
        yield Results
