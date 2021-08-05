
from otree.api import *
c = cu

doc = 'Introduction & risk attitude game'
class Constants(BaseConstants):
    name_in_url = 'risk_attitude'
    players_per_group = None
    num_rounds = 1
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass
class Player(BasePlayer):
    pass
class Introduction(Page):
    form_model = 'player'
page_sequence = [Introduction]