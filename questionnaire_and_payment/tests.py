from otree.api import Bot, expect

from . import Questionnaire, Payments


class PlayerBot(Bot):
    def play_round(self):
        yield Questionnaire, {
            "age": 18,
            "gender": "Other",
            "sid": "ab12345",
            "years_service": 0,
            "residence": "City",
            "people_known": "Around half",
            "lottery_understanding": "Average",
            "interative_understanding": "Average",
            "interactive_others": "Difficult to say",
            "volunteer_work": "No",
        }
        expect(
            "<p>Thank you again for taking part in this experimental session today.</p>",
            "in",
            self.html,
        )
        assert "points" not in str(self.html), "Oops - points not tokens"
        yield Payments
