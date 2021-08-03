
from otree.api import *
c = cu

doc = ''
class Constants(BaseConstants):
    name_in_url = 'my_survey'
    players_per_group = None
    num_rounds = 1
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
page_sequence = [Survey, Results]