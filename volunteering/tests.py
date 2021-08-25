from otree.api import Bot, expect

from . import Instructions, Understanding, Understood, Volunteering, Results


class PlayerBot(Bot):

    cases = ["never", "all"]
    pre_game_payoff = {}

    def play_round(self):
        if self.session.config["name"] == "farmer_framing":
            # framing=0 gives False, farmers
            expect(self.session.config.get('framing', None), 0)
        elif self.session.config["name"] == "community_centre_framing":
            # framing=1 gives True, Community Centre
            expect(self.session.config.get('framing', None), 1)
        volunteering_framing = bool(self.session.config.get('framing', 0))
        if volunteering_framing:
            right_framing = "community centre"
            wrong_framing = "farmer"
        else:
            right_framing = "farmer"
            wrong_framing = "community centre"
        if self.round_number == 1:
            assert ("community centre" in str(self.html).lower() or "farmer" in str(self.html).lower()), str(self.html)
            expect(wrong_framing, "not in", self.html)
            expect(right_framing, "in", self.html)
            yield Instructions
            yield Understanding, {
                "understanding1": 0,
                "understanding2": 50,
                "understanding3": 0,
            }
            yield Understood
        # yield WaitToStart <-- automatic
        if self.case == "never":
            # Do with timeout?
            yield Volunteering, {"volunteer": False}
            expect("<p>Thanks for making your choice.</p>", "in", self.html)
            expect(
                "No one in your group volunteered. You earn 0 points.",
                "in",
                self.html,
            )
            expect(self.player.payoff, 0)
        else:
            yield Volunteering, {"volunteer": True}
            expect("<p>Thanks for making your choice.</p>", "in", self.html)
            if self.round_number == 1:
                # Cache this for checking total at the end of this game/app
                self.pre_game_payoff[self.participant.id] = (
                    self.participant.payoff - self.player.payoff
                )
            if self.player.id_in_group == 1:
                # Appears bot for player one is always first
                expect("You volunteered first.", "in", self.html)
                if self.round_number in [1, 2, 5]:
                    expect(self.player.payoff, 0)  # self-less
                else:
                    expect(self.player.payoff, 50)  # compensated
                if self.round_number == 5:
                    # Game over, 0 + 0 + 50 + 50 + 0
                    expect(
                        self.participant.payoff,
                        100 + self.pre_game_payoff[self.participant.id],
                    )
            else:
                expect(
                    "You volunteered but another person in your group volunteered before you.", "in", self.html
                )
                if self.round_number in [1, 2, 5]:
                    expect(self.player.payoff, 50)  # free-loader
                else:
                    expect(self.player.payoff, 40)  # compensation deduction
                if self.round_number == 5:
                    # Game over, 50 + 50 + 40 + 40 + 50
                    expect(
                        self.participant.payoff,
                        230 + self.pre_game_payoff[self.participant.id],
                    )
        # Check wording in the results / next round instructions:
        expect(wrong_framing, "not in", self.html)
        yield Results
