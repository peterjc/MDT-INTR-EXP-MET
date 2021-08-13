
from otree.api import *
c = cu

doc = 'Introduction & risk attitude lottery game based on Holt and Laury (2002).'
class Constants(BaseConstants):
    name_in_url = 'risk_attitude'
    players_per_group = None
    num_rounds = 1
    payoff_red_A = 40
    payoff_white_A = 32
    payoff_red_B = 77
    payoff_white_B = 2
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass
def lottery_choices(player):
    return [
        [True, f'A: 🔴 = {Constants.payoff_red_A}, ⚪ = {Constants.payoff_white_A}'],
        [False, f'B: 🔴 = {Constants.payoff_red_B}, ⚪ = {Constants.payoff_white_B}']
    ]
def lottery1_choices(player):
    return lottery_choices(player)
def lottery2_choices(player):
    return lottery_choices(player)
def lottery3_choices(player):
    return lottery_choices(player)
def lottery4_choices(player):
    return lottery_choices(player)
def lottery5_choices(player):
    return lottery_choices(player)
def lottery6_choices(player):
    return lottery_choices(player)
def lottery7_choices(player):
    return lottery_choices(player)
def lottery8_choices(player):
    return lottery_choices(player)
def lottery9_choices(player):
    return lottery_choices(player)
def lottery10_choices(player):
    return lottery_choices(player)
class Player(BasePlayer):
    lottery1 = models.BooleanField()
    lottery2 = models.BooleanField()
    lottery3 = models.BooleanField()
    lottery4 = models.BooleanField()
    lottery5 = models.BooleanField()
    lottery6 = models.BooleanField()
    lottery7 = models.BooleanField()
    lottery8 = models.BooleanField()
    lottery9 = models.BooleanField()
    lottery10 = models.BooleanField()
    lottery_selected = models.IntegerField()
    lottery_red = models.BooleanField()
class Introduction(Page):
    form_model = 'player'
    @staticmethod
    def vars_for_template(player):
        session = player.session
        from otree.settings import REAL_WORLD_CURRENCY_CODE
        from otree.currency import RealWorldCurrency
        factor = cu(1 / player.session.config['real_world_currency_per_point'])
        rate = f"{REAL_WORLD_CURRENCY_CODE} at a rate of {RealWorldCurrency(1)} per every {factor}"
        return {"rate": rate}
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