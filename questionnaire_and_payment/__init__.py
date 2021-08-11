
from otree.api import *
c = cu

doc = 'Show questionnaire (including payment details) and report payoffs. Needs to get payoff information from previous apps.'
class Constants(BaseConstants):
    name_in_url = 'questionnaire_and_payment'
    players_per_group = None
    num_rounds = 1
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass
class Player(BasePlayer):
    age = models.IntegerField(label='What is your age?', min=18)
    gender = models.StringField(choices=[['Male', 'Male'], ['Female', 'Female'], ['Other', 'Other'], ['Prefer not to say', 'Prefer not to say']], label='What is your gender?')
    years_service = models.IntegerField(label='How many years have you been working at the James Hutton Insititute?', min=0)
    people_known = models.StringField(choices=[['None or almost none', 'None or almost none'], ['Less than half', 'Less than half'], ['Around half', 'Around half'], ['More than half', 'More than half'], ['Almost everyone or everyone', 'Almost everyone or everyone']], label='How many people do you know among those in today’s session?')
    lottery_understanding = models.StringField(choices=[['Not at all', 'Not at all'], ['A little', 'A little'], ['Average', 'Average'], ['Quite well', 'Quite well'], ['Completely', 'Completely']], label='How much do you believe that you understood the instructions of the lottery game? ')
    interative_understanding = models.StringField(choices=[['Not at all', 'Not at all'], ['A little', 'A little'], ['Average', 'Average'], ['Quite well', 'Quite well'], ['Completely', 'Completely']], label='How much do you believe that you understood the instructions of the interactive game?')
    interactive_others = models.StringField(choices=[['They did not volunteer regardless of the incentive', 'They did not volunteer regardless of the incentive'], ['They volunteered in the non-incentivised rounds, and did not volunteer in the incentivised rounds', 'They volunteered in the non-incentivised rounds, and did not volunteer in the incentivised rounds'], ['They volunteered in the incentivised rounds, and did not volunteer in the non-incentivised rounds', 'They volunteered in the incentivised rounds, and did not volunteer in the non-incentivised rounds'], ['They volunteered regardless of the incentive', 'They volunteered regardless of the incentive'], ['Difficult to say', 'Difficult to say']], label='How do you think that most of the participants in your group played the interactive game?')
    volunteer_work = models.StringField(choices=[['Yes regularly', 'Yes regularly'], ['Yes but not regularly', 'Yes but not regularly'], ['No', 'No']], label='Do you engage in volunteer work in your community?')
    residence = models.StringField(choices=[['City', 'City'], ['Accessible town', 'Accessible town'], ['Remote town', 'Remote town'], ['Accessible rural', 'Accessible rural'], ['Remote rural', 'Remote rural']], label='Where do you reside?')
    sid = models.StringField(label='Staff Identification Number (SID)')
class Questionnaire(Page):
    form_model = 'player'
    form_fields = ['sid', 'age', 'gender', 'residence', 'years_service', 'people_known', 'lottery_understanding', 'interative_understanding', 'interactive_others', 'volunteer_work']
class Payments(Page):
    form_model = 'player'
page_sequence = [Questionnaire, Payments]