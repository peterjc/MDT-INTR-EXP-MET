
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
    lottery1 = models.BooleanField(label='1')
    lottery2 = models.BooleanField(label='2')
    lottery3 = models.BooleanField(label='3')
    lottery4 = models.BooleanField(label='4')
    lottery5 = models.BooleanField(label='5')
    lottery6 = models.BooleanField(label='6')
    lottery7 = models.BooleanField(label='7')
    lottery8 = models.BooleanField(label='8')
    lottery9 = models.BooleanField(label='9')
    lottery10 = models.BooleanField(label='10')
class Introduction(Page):
    form_model = 'player'
class LotteryInstructions(Page):
    form_model = 'player'
class LotteryDecision(Page):
    form_model = 'player'
    form_fields = ['lottery1', 'lottery2', 'lottery3', 'lottery4', 'lottery5', 'lottery6', 'lottery7', 'lottery8', 'lottery9', 'lottery10']
page_sequence = [Introduction, LotteryInstructions, LotteryDecision]