
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
    volunteer = models.BooleanField(choices=[[True, 'Yes'], [False, 'No']], initial=False, label='Do you volunteer?')
    submission_timestamp = models.FloatField()
class Survey(Page):
    form_model = 'player'
    form_fields = ['name', 'age']
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1
class Instructions(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1
class Volunteering(Page):
    form_model = 'player'
    form_fields = ['volunteer']
    timeout_seconds = 15
    timer_text = 'You have 15 seconds to decide.'
    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        if player.round_number == 1:
            # Record the name on the long lived participant object
            participant.name = player.name
        else:
            # Pull back the name (since only asking once)
            player.name = participant.name
        
        import time  # hack, want this at top level really
        player.submission_timestamp = time.time()
class Results(Page):
    form_model = 'player'
    @staticmethod
    def vars_for_template(player):
        session = player.session
        subsession = player.subsession
        group = player.group
        # Rules and payoff depend on round...
        # Was this player first to volunteer?
        players = subsession.get_players()
        if not any(p.volunteer for p in players):
            msg = "No one in your group volunteered."
        elif player.submission_timestamp == min(p.submission_timestamp for p in players if p.volunteer):
            msg = "You volunteered first."
        else:
            msg = "At least one person in your group volunteered first."
        return {"message": msg}
page_sequence = [Survey, Instructions, Volunteering, Results]