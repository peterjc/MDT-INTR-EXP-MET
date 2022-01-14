
from otree.api import *
c = cu

doc = 'Show questionnaire (and collect payment details), report payoffs from previous apps.'
class C(BaseConstants):
    NAME_IN_URL = 'questionnaire_and_payment'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass
class Player(BasePlayer):
    age = models.IntegerField(label='What is your age?', min=18)
    gender = models.StringField(choices=[['Male', 'Male'], ['Female', 'Female'], ['Other', 'Other'], ['Prefer not to say', 'Prefer not to say']], label='What is your gender?')
    years_service = models.IntegerField(label='How many years have you been working at the James Hutton Institute?', min=0)
    lottery_understanding = models.StringField(choices=[['Not at all', 'Not at all'], ['A little', 'A little'], ['Average', 'Average'], ['Quite well', 'Quite well'], ['Completely', 'Completely']], label='How much did you understand the instructions of the lottery game?')
    interative_understanding = models.StringField(choices=[['Not at all', 'Not at all'], ['A little', 'A little'], ['Average', 'Average'], ['Quite well', 'Quite well'], ['Completely', 'Completely']], label='How much did you understand the instructions of the interactive game?')
    interactive_others = models.StringField(choices=[['They did not volunteer regardless of the incentive', 'They did not volunteer, regardless of the round'], ['They volunteered in the non-incentivised rounds, and did not volunteer in the incentivised rounds', 'They volunteered only in the rounds where the volunteer was NOT receiving additional points'], ['They volunteered in the incentivised rounds, and did not volunteer in the non-incentivised rounds', 'They volunteered only in the rounds where the volunteer was receiving additional points'], ['They volunteered regardless of the incentive', 'They volunteered regardless of the round”'], ['Difficult to say', 'Difficult to say']], label='How do you think that most of the participants in your group played the interactive game?')
    volunteer_work = models.StringField(choices=[['Yes regularly', 'Yes regularly'], ['Yes but not regularly', 'Yes but not regularly'], ['No', 'No']], label='Do you engage in volunteer work in your community?')
    residence = models.StringField(choices=[['City', 'City'], ['Accessible town', 'Accessible town'], ['Remote town', 'Remote town'], ['Accessible rural', 'Accessible rural'], ['Remote rural', 'Remote rural']], label='Where do you reside?')
    sid = models.StringField(label='Staff Identification Number (SID), or email address for participants without one:')
class Questionnaire(Page):
    form_model = 'player'
    form_fields = ['sid', 'age', 'gender', 'residence', 'years_service', 'lottery_understanding', 'interative_understanding', 'interactive_others', 'volunteer_work']
class Payments(Page):
    form_model = 'player'
    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        # The risk_attitude & volunteer_community_centre app recorded these strings:
        return {
            "risk_attitude_msg": participant.risk_attitude_msg,
            "volunteering_msg": participant.volunteering_msg,
        }
class TheEnd(Page):
    form_model = 'player'
page_sequence = [Questionnaire, Payments, TheEnd]