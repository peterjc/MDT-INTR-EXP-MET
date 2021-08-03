
from otree.api import *
c = cu

doc = 'Multi-round volunteer dilemma framed as running a community centre.'
class Constants(BaseConstants):
    name_in_url = 'volunteer_community_centre'
    players_per_group = 6
    num_rounds = 5
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass
class Player(BasePlayer):
    name = models.StringField(label='What is your name?')
    age = models.IntegerField(label='What is your age?', min=18)
class Survey(Page):
    form_model = 'player'
    form_fields = ['name', 'age']
class Results(Page):
    form_model = 'player'
class Instructions(Page):
    form_model = 'player'
class Volunteering(Page):
    form_model = 'player'
    form_fields = ['age', 'name']
    timeout_seconds = 15
    timer_text = 'You have 15 seconds to decide.'
page_sequence = [Survey, Results, Instructions, Volunteering]