
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
    volunteer = models.BooleanField(choices=[[True, 'Yes'], [False, 'No']], initial=False, label='Do you volunteer?')
    submission_timestamp = models.FloatField()
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
        Imagine that the {Constants.num_rounds} people in your group reside in the same small rural community. In your community there is a community centre where people can meet during the day to have a coffee together and do a series of activities. All the residents have access to the centre but in order to enjoy this space, someone must open it and prepare the rooms as well as make order and clean afterwards. If no one volunteers to do this, the centre remains closed. The activities implemented in the centre generate a benefit to the residents attending, which we quantify in 50 tokens, while the volunteers incur in personal costs in terms of time and energy.
        </p>
        <p>
        Do you have any questions? If so, please raise your hand virtually.
        </p>
        <p>
        Now we will play round {player.round_number} of the game. The countdown will start once all {Constants.num_rounds} members of your group have clicked the "Next" button below. To volunteer, you need to click on the "Volunteer" button at the centre of the page. Regardless of your choice, you will have to wait until the end of the {Constants.volunteer_timeout} seconds. When you are ready, please click on the "Next" button below. The instructions will remain available at the bottom of the page.
        </p>
        """
        else:
            msg = f"ERROR - Invalid round number {player.round_number}"
        return {"instructions": msg}
class WaitToStart(WaitPage):
    title_text = 'Waiting for other players to begin'
class Volunteering(Page):
    form_model = 'player'
    form_fields = ['volunteer']
    timeout_seconds = 15
    timer_text = 'You have 15 seconds to decide.'
    @staticmethod
    def before_next_page(player, timeout_happened):
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
        participant = player.participant
        # Rules and payoff depend on round...
        msg = "<p>Thanks for making your choice.</p>"
        # Was this player first to volunteer?
        players = subsession.get_players()
        if player.round_number in [1, 2, 5]:
            # Initial rules - self-less volunteer
            no_volunteers_payoff = 0
            volunteer_payoff = 0
            group_payoff = 50
            if not any(p.volunteer for p in players):
                player.payoff = no_volunteers_payoff
                msg += f"<p>No one in your group volunteered. You earned {no_volunteers_payoff} tokens.</p>"
            elif player.submission_timestamp == min(p.submission_timestamp for p in players if p.volunteer):
                player.payoff = volunteer_payoff
                msg += f"<p>You volunteered first. You earn {volunteer_payoff} tokens and the other members of your group earn {group_payoff}.</p>"
            else:
                player.payoff = group_payoff
                msg += f"<p>Another person in your group volunteered first. You earn {group_payoff} tokens.</p>"
        elif player.round_number in [3, 4]:
            # Alternative rules - compensated volunteer
            no_volunteers_payoff = 0
            volunteer_payoff = 50
            group_payoff = 40
            if not any(p.volunteer for p in players):
                player.payoff = no_volunteers_payoff
                msg += f"<p>No one in your group volunteered. You earned {no_volunteers_payoff} tokens.</p>"
            elif player.submission_timestamp == min(p.submission_timestamp for p in players if p.volunteer):
                player.payoff = volunteer_payoff
                msg += f"<p>You volunteered first. You earn {volunteer_payoff} tokens and the other members of your group earn {group_payoff} tokens.</p>"
            else:
                player.payoff = group_payoff
                msg += f"<p>Another person in your group volunteered first. You earn {group_payoff} tokens, and the person who volunteered first earns {volunteer_payoff} tokens.</p>"
        else:
            raise RuntimeError(f"ERROR - Unexpected round number {player.round_number}")
        
        # Now record the payoff for use in later app to report the payoff breakdown:
        if player.round_number == 1:
            participant.volunteer_community_centre = [None] * Constants.num_rounds
        participant.volunteer_community_centre[player.round_number - 1] = int(player.payoff)
        
        if player.round_number == 1:
            msg += """
        <p>Now we will play a second round of the game, which will follow exactly the same rules of this one. The second round will start when everyone in your group has clicked on "Next" the button below, which will redirect you to a new page with the countdown. Again, you can volunteer for your group by clicking on the ‘Volunteer’ button. When you are ready, please click on the "Next" button below.</p>
        """
        elif player.round_number == 2:
            # TODO - pull scores from code?
            msg += """
        <p>Now we will play a third round of the game, which will follow slightly different rules. Again, at least one person in your group needs to volunteer in order for you to earn some tokens, meaning that if no one volunteers, no one will earn any tokens. However, in this third round the volunteer will earn 50 tokens, while the other participants will earn 40 tokens. Only the participant who will volunteer first will earn the 50 tokens; if you decide to volunteer but someone else has volunteered before you, you will earn 40 tokens. This is because the volunteer will have to pay 50 tokens, but all of the other participants will transfer 10 of their 50 tokens to the volunteer. Imagine that your small rural community has decided that to access the community centre, residents have to pay a fee, which will be used to compensate the person who prepares the rooms and tides up afterwards.</p>
        <p>Do you have any questions? If so, please raise your hand virtually. A member of the experimental team will answer your question for everyone.</p>
        <p>The third round will start when everyone in your group has clicked on "Next" the button below, which will redirect you to a new page with the countdown. Again, you can volunteer for your group by clicking on the "Volunteer" button. When you are ready, please click on the "Next" button below. The instructions will remain available at the bottom of the page</p>
        """
        elif player.round_number == 3:
            msg += """
        <p>Now we will play a fourth round of the game, which will follow exactly the same rules of the third one. The fourth round will start when everyone in your group has clicked on "Next" the button below, which will redirect you to a new page with the countdown. Again, you can volunteer for your group by clicking on the ‘Volunteer’ button. When you are ready, please click on the "Next" button below.</p>
        """
        elif player.round_number == 4:
            # TODO - pull scores from code?
            msg += """
        <p>Now we will play the final round of this game, which will follow exactly the same rules of the first two rounds. The volunteer will have to pay a cost of 50 tokens, meaning that they will not earn any tokens. If at least one participant volunteers, everyone apart from them will earn 50 tokens. Only the participant who volunteers first will have to pay the 50 tokens, and thus overall will not earn any tokens. Anyone who volunteers after them will earn 50 tokens. If no one volunteers, no one will earn any tokens. Imagine that after some discussions, it was decided in your community to lift the fee for attending the community centre; therefore, the volunteer will not be compensated any more.</p>
        <p>The final round will start when everyone in your group has clicked on "Next" the button below, which will redirect you to a new page with the countdown. Again, you can volunteer for your group by clicking on the "Volunteer" button. When you are ready, please click on the "Next" button below. The instructions will remain available at the bottom of the page.</p>
        """
        elif player.round_number == 5:
            msg += """
        <p>The game session has finished. Please click on the "Next" button below, and you will be redirected to a short questionnaire, after which you will be communicated your earnings.</p>
        """
        else:
            raise RuntimeError(f"ERROR - unexpected round number {player.round_number}")
        return {"message": msg}
page_sequence = [Instructions, WaitToStart, Volunteering, Results]