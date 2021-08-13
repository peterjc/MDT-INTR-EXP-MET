
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
    lottery1 = models.BooleanField(choices=[[True, 'A: 🔴 = 100, ⚪ = 80'], [False, 'B: 🔴 = 190, ⚪ = 5']], label='1')
    lottery2 = models.BooleanField(choices=[[True, 'A: 🔴 = 100, ⚪ = 80'], [False, 'B: 🔴 = 190, ⚪ = 5']], label='2')
    lottery3 = models.BooleanField(choices=[[True, 'A: 🔴 = 100, ⚪ = 80'], [False, 'B: 🔴 = 190, ⚪ = 5']], label='3')
    lottery4 = models.BooleanField(choices=[[True, 'A: 🔴 = 100, ⚪ = 80'], [False, 'B: 🔴 = 190, ⚪ = 5']], label='4')
    lottery5 = models.BooleanField(choices=[[True, 'A: 🔴 = 100, ⚪ = 80'], [False, 'B: 🔴 = 190, ⚪ = 5']], label='5')
    lottery6 = models.BooleanField(choices=[[True, 'A: 🔴 = 100, ⚪ = 80'], [False, 'B: 🔴 = 190, ⚪ = 5']], label='6')
    lottery7 = models.BooleanField(choices=[[True, 'A: 🔴 = 100, ⚪ = 80'], [False, 'B: 🔴 = 190, ⚪ = 5']], label='7')
    lottery8 = models.BooleanField(choices=[[True, 'A: 🔴 = 100, ⚪ = 80'], [False, 'B: 🔴 = 190, ⚪ = 5']], label='8')
    lottery9 = models.BooleanField(choices=[[True, 'A: 🔴 = 100, ⚪ = 80'], [False, 'B: 🔴 = 190, ⚪ = 5']], label='9')
    lottery10 = models.BooleanField(choices=[[True, 'A: 🔴 = 100, ⚪ = 80'], [False, 'B: 🔴 = 190, ⚪ = 5']], label='10')
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
        participant = player.participant
        # Will now randomly pick one of the 10 lotteries,
        # randomly pick a red or white ball, and apply A/B payoffs
        import random  # TODO - import at top level if possible
        lottery_selected = random.randint(1, 10)
        # Run the lottery, red (i balls) or white (10-i balls)?
        lottery_red = random.randint(1, 10) <= lottery_selected
        # There ought to be a built in list of fields to avoid this lookup:
        lottery_choice = bool([
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
        ][lottery_selected - 1])
        if lottery_choice:
            # Apply A scores
            player.payoff = Constants.payoff_red_A if lottery_red else Constants.payoff_white_A
        else:
            # Apply B scores
            player.payoff = Constants.payoff_red_B if lottery_red else Constants.payoff_white_B
        
        # Record in the player fields for logging in the DB
        player.lottery_selected = lottery_selected
        player.lottery_red = lottery_red
        
        # Finally, record this in participant.risk_attitude for the final app report
        participant.risk_attitude = {
            "lottery_red": lottery_red,
            "lottery_selected": lottery_selected,
            "lottery_choice": lottery_choice,
            "lottery_payoff": int(player.payoff)
        }
page_sequence = [Introduction, LotteryInstructions, LotteryDecision]