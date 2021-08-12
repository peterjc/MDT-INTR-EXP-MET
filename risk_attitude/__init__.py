
from otree.api import *
c = cu

doc = 'Introduction & risk attitude game'
class Constants(BaseConstants):
    name_in_url = 'risk_attitude'
    players_per_group = None
    num_rounds = 1
    payoff_red_A = 100
    payoff_white_A = 80
    payoff_red_B = 190
    payoff_white_B = 5
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass
class Player(BasePlayer):
    lottery1 = models.BooleanField(choices=[[True, 'A: Red = 100, White = 80'], [False, 'B: Red = 190, White = 5']], label='1')
    lottery2 = models.BooleanField(choices=[[True, 'A: Red = 100, White = 80'], [False, 'B: Red = 190, White = 5']], label='2')
    lottery3 = models.BooleanField(choices=[[True, 'A: Red = 100, White = 80'], [False, 'B: Red = 190, White = 5']], label='3')
    lottery4 = models.BooleanField(choices=[[True, 'A: Red = 100, White = 80'], [False, 'B: Red = 190, White = 5']], label='4')
    lottery5 = models.BooleanField(choices=[[True, 'A: Red = 100, White = 80'], [False, 'B: Red = 190, White = 5']], label='5')
    lottery6 = models.BooleanField(choices=[[True, 'A: Red = 100, White = 80'], [False, 'B: Red = 190, White = 5']], label='6')
    lottery7 = models.BooleanField(choices=[[True, 'A: Red = 100, White = 80'], [False, 'B: Red = 190, White = 5']], label='7')
    lottery8 = models.BooleanField(choices=[[True, 'A: Red = 100, White = 80'], [False, 'B: Red = 190, White = 5']], label='8')
    lottery9 = models.BooleanField(choices=[[True, 'A: Red = 100, White = 80'], [False, 'B: Red = 190, White = 5']], label='9')
    lottery10 = models.BooleanField(choices=[[True, 'A: Red = 100, White = 80'], [False, 'B: Red = 190, White = 5']], label='10')
    lottery_selected = models.IntegerField()
    lottery_red = models.BooleanField()
class Introduction(Page):
    form_model = 'player'
class LotteryInstructions(Page):
    form_model = 'player'
class LotteryDecision(Page):
    form_model = 'player'
    form_fields = ['lottery1', 'lottery2', 'lottery3', 'lottery4', 'lottery5', 'lottery6', 'lottery7', 'lottery8', 'lottery9', 'lottery10']
    @staticmethod
    def before_next_page(player, timeout_happened):
        # Will now randomly pick one of the 10 lotteries,
        # randomly pick a red or white ball, and apply A/B payoffs
        # Record the random selections for use in the test suite.
        import random  # TODO - import at top level if possible
        player.lottery_selected = random.randint(1, 10)
        # Run the lottery, red (i balls) or white (10-i balls)?
        player.lottery_red = random.randint(1, 10) <= player.lottery_selected
        # There ought to be a built in list of fields to avoid this lookup:
        if [
            player.lottery1,
            player.lottery2,
            player.lottery3,
            player.lottery4,
            player.lottery5,
            player.lottery6,
            player.lottery7,
            player.lottery8,
            player.lottery9,
            player.lottery10,
        ][player.lottery_selected - 1]:
            # Apply A scores
            player.payoff = Constants.payoff_red_A if player.lottery_red else Constants.payoff_white_A
        else:
            # Apply B scores
            player.payoff = Constants.payoff_red_B if player.lottery_red else Constants.payoff_white_B
        
page_sequence = [Introduction, LotteryInstructions, LotteryDecision]