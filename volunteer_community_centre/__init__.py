
from otree.api import *
c = cu

doc = 'Multi-round volunteer dilemma framed as running a community centre.'
class Constants(BaseConstants):
    name_in_url = 'volunteer_community_centre'
    players_per_group = 6
    num_rounds = 5
    volunteer_timeout = 15
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
    @staticmethod
    def vars_for_template(player):
        group = player.group
        participant = player.participant
        if player.round_number == 1:
            msg = f"""
        <p>
        Thank you for playing the first game. Now we will play a second game.
        </p>
        <p>
        This game consists of {Constants.num_rounds} rounds. In each round, you will receive instructions and will be asked to make a decision. The decisions in each round are completely independent from each other. Your earnings from each round will depend on your decision, as well as the decisions that other participants in that round.
        </p>
        <p>
        The computer will pair you with other {Constants.players_per_group - 1} participants, making a group of {Constants.players_per_group}. The group will remain the same during the {Constants.num_rounds} rounds. In each round, each of the members of your group has the opportunity to earn 50 tokens. In order for the members of your group to earn the 50 tokens, at least one of you needs to "volunteer". The volunteer will have to pay a cost of 50 tokens, meaning that they will not earn any tokens in that round. You will have {Constants.volunteer_timeout} seconds to decide whether to volunteer. If at least one participant in your group volunteers, everyone apart from them will earn 50 tokens. Only the participant who volunteers first will have to pay the 50 tokens, and thus will not earn any token. Those who will possibly volunteer after them will receive 50 tokens. If no one volunteers, no one will earn any token. At the end of the {Constants.volunteer_timeout} seconds, you will be automatically redirected to the page with the results of that round. You will be communicated whether anyone has volunteered, and your total earnings in that round. You will not know the identity of the person who has volunteered.
        </p>
        <p>
        Imagine that the six people in your group reside in the same small rural community. In your community there is a community centre where people can meet during the day to have a coffee together and do a series of activities. All the residents have access to the centre but in order to enjoy this space, someone must open it and prepare the rooms as well as make order and clean afterwards. If no one volunteers to do this, the centre remains closed. The activities implemented in the centre generate a benefit to the residents attending, which we quantify in 50 tokens, while the volunteers incur in personal costs in terms of time and energy.
        </p>
        <p>
        Do you have any questions? If so, please raise your hand virtually.
        </p>
        <p>
        Now we will play the first round of the game. The countdown will start once all the six members of your group have clicked the "Next" button below. To volunteer, you need to click on the "Volunteer" button at the centre of the page. Regardless of your choice, you will have to wait until the end of the {Constants.volunteer_timeout} seconds. When you are ready, please click on the "Next" button below. The instructions will remain available at the bottom of the page.
        </p>
        """
        else:
            msg = f"ERROR - Invalid round number {player.round_number}"
        return {"instructions": msg}
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
    @staticmethod
    def get_timeout_seconds(player):
        return Constants.volunteer_timeout
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