
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
def record_round_start(group):
    import time
    group.start_timestamp = time.time()
class Group(BaseGroup):
    start_timestamp = models.FloatField()
def understanding1_error_message(player, value):
    group = player.group
    if value != 0:
        return f"Your answer is wrong, if no one in the group volunteers all of you earn {cu(0)}"
def understanding2_error_message(player, value):
    if value != 50:
        return f"Your answer is wrong, if someone volunteers before you, they will earn {cu(0)} but you will still earn {cu(50)}"
def understanding3_error_message(player, value):
    if value != 0:
        return f"Your answer is wrong, if you are the first person to volunteer, you earn {cu(0)}"
class Player(BasePlayer):
    volunteer = models.BooleanField(choices=[[True, 'Yes'], [False, 'No']], initial=False, label='Do you volunteer?')
    submission_timestamp = models.FloatField()
    understanding1 = models.IntegerField(label='No one in your group volunteers within the time available. How many points will you earn?', min=0)
    understanding2 = models.IntegerField(label='You volunteer but someone else has volunteered before you. How many points will you earn? ', min=0)
    understanding3 = models.IntegerField(label='How many points will you earn if you volunteer first?', min=0)
class Instructions(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1
    @staticmethod
    def vars_for_template(player):
        group = player.group
        participant = player.participant
        from otree.settings import POINTS_CUSTOM_NAME
        units = POINTS_CUSTOM_NAME if POINTS_CUSTOM_NAME else "points"
        if player.round_number == 1:
            msg = f"""
        <p>
        Thank you for playing the first game. Now we will play a second game.
        </p>
        <p>
        This game consists of {Constants.num_rounds} rounds. In each round, you will receive instructions and will be asked to make a decision. The decisions in each round are completely independent from each other. Your earnings from each round will depend on your decision, as well as the decisions that other participants make in that round.
        </p>
        <p>
        The computer will pair you with other {Constants.players_per_group - 1} participants, making a group of {Constants.players_per_group}. The group will remain the same during the {Constants.num_rounds} rounds. In each round, each of the members of your group has the opportunity to earn {cu(50)}. In order for the members of your group to earn the {cu(50)}, at least one of you needs to "volunteer". The volunteer will have to pay a cost of {cu(50)}, meaning that they will not earn any {units} in that round. You will have {Constants.volunteer_timeout} seconds to decide whether to volunteer. If at least one participant in your group volunteers, everyone apart from them will earn {cu(50)}. Only the participant who volunteers first will have to pay the {cu(50)}, and thus will not earn any {units}. Those who will possibly volunteer after them will  not be considered as volunteers and will thus receive {cu(50)}. If no one volunteers, no one will earn any {units}. At the end of the {Constants.volunteer_timeout} seconds, you will be automatically redirected to the page with the results of that round. You will be communicated whether anyone has volunteered, and your total earnings in that round. You will not know the identity of the person who has volunteered.
        </p>
        <p>
        Imagine that the {Constants.num_rounds} people in your group reside in the same small rural community. In your community there is a community centre where people can meet during the day to have a coffee together and do a series of activities. All the residents have access to the centre but in order to enjoy this space, someone must open it and prepare the rooms as well as make order and clean afterwards. If no one volunteers to do this, the centre remains closed. The activities implemented in the centre benefit the residents attending.  This benefit has a value of {cu(50)}, while the volunteers incur personal costs in terms of time and energy that cancel out the benefits from the activities implemented in the centre.
        </p>
        <p>
        Do you have any questions? If so, please raise your hand virtually.
        </p>
        <p>
        Now please click ‘Next’, and you will be redirected to a page with questions to check your understanding of the instructions.
        </p>
        """
            participant.volunteer_community_centre_msg = msg  # cache for reminder when Volunteering
        else:
            msg = f"ERROR - Invalid round number {player.round_number}"
        return {"instructions": msg}
class Understanding(Page):
    form_model = 'player'
    form_fields = ['understanding1', 'understanding2', 'understanding3']
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1
class Understood(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1
class WaitToStart(WaitPage):
    after_all_players_arrive = 'record_round_start'
    title_text = 'Waiting for other players to begin'
class Volunteering(Page):
    form_model = 'player'
    form_fields = ['volunteer']
    timer_text = 'You have 15 seconds to decide.'
    @staticmethod
    def is_displayed(player):
        group = player.group
        # Expecting will always be (just under) 15s left,
        import time
        return Constants.volunteer_timeout - time.time() + group.start_timestamp > 1
    @staticmethod
    def vars_for_template(player):
        participant = player.participant
        # In round 1, the Volunteering page recorded the instructions here.
        # After each round we set this up in the Results page for the next round
        return {"instructions": participant.volunteer_community_centre_msg}
    @staticmethod
    def before_next_page(player, timeout_happened):
        group = player.group
        import time  # hack, want this at top level really
        # Convert to a relative timestamp (in seconds):
        player.submission_timestamp = time.time() - group.start_timestamp
    @staticmethod
    def get_timeout_seconds(player):
        group = player.group
        import time
        return Constants.volunteer_timeout - time.time() + group.start_timestamp
class Results(Page):
    form_model = 'player'
    @staticmethod
    def vars_for_template(player):
        session = player.session
        subsession = player.subsession
        group = player.group
        participant = player.participant
        from otree.settings import POINTS_CUSTOM_NAME
        units = POINTS_CUSTOM_NAME if POINTS_CUSTOM_NAME else "points"
        # Rules and payoff depend on round...
        instructions = "<p>Click the button to volunteer, or wait for the timer to finish.</p>"
        msg = "<p>Thanks for making your choice.</p>"
        # Was this player first to volunteer?
        players = subsession.get_players()
        if player.round_number in [1, 2, 5]:
            # Initial rules - self-less volunteer
            no_volunteers_payoff = cu(0)
            volunteer_payoff = cu(0)
            group_payoff = cu(50)
            if not any(p.volunteer for p in players):
                player.payoff = no_volunteers_payoff
                msg += f"<p>No one in your group volunteered. You earn {no_volunteers_payoff}.</p>"
            elif not player.volunteer:
                player.payoff = group_payoff
                msg += f"<p>You did not volunteer but at least one person in your group volunteered. You earn {group_payoff}.</p>"
            elif player.submission_timestamp == min(p.submission_timestamp for p in players if p.volunteer):
                player.payoff = volunteer_payoff
                msg += f"<p>You volunteered first. You earn {volunteer_payoff} and the other members of your group earn {group_payoff}.</p>"
            else:
                player.payoff = group_payoff
                msg += f"<p>You volunteered but another person in your group volunteered before you. You earn {group_payoff}.</p>"
        elif player.round_number in [3, 4]:
            # Alternative rules - compensated volunteer
            no_volunteers_payoff = cu(0)
            volunteer_payoff = cu(50)
            group_payoff = cu(40)
            if not any(p.volunteer for p in players):
                player.payoff = no_volunteers_payoff
                msg += f"<p>No one in your group volunteered. You earn {no_volunteers_payoff}.</p>"
            elif not player.volunteer:
                player.payoff = group_payoff
                msg += f"<p>You did not volunteer but at least one person in your group volunteered. You earn {group_payoff}, and the person who volunteered first earns {volunteer_payoff}.</p>"
            elif player.submission_timestamp == min(p.submission_timestamp for p in players if p.volunteer):
                player.payoff = volunteer_payoff
                msg += f"<p>You volunteered first. You earn {volunteer_payoff} and the other members of your group earn {group_payoff}.</p>"
            else:
                player.payoff = group_payoff
                msg += f"<p>You volunteered but another person in your group volunteered before you. You earn {group_payoff}, and the person who volunteered first earns {volunteer_payoff}.</p>"
        else:
            raise RuntimeError(f"ERROR - Unexpected round number {player.round_number}")
        # Instructions change round by round...
        if player.round_number == 1:
            instructions = """
        <p>Now we will play a second round of the game, which will follow exactly the same rules of this one. The second round will start when everyone in your group has clicked on "Next" the button below, which will redirect you to a new page with the countdown. Again, you can volunteer for your group by clicking on the ‘Volunteer’ button. When you are ready, please click on the "Next" button below.</p>
        """
        elif player.round_number == 2:
            # TODO - pull scores from code? Tricky as this is about the NEXT round
            instructions = f"""
        <p>Now we will play a third round of the game, which will follow slightly different rules. Again, at least one person in your group needs to volunteer in order for you to earn some {units}, meaning that if no one volunteers, no one will earn any {units}. As previously, if there is a volunteer, all other participants benefit by {cu(50)}. However, in this round, all of the other participants will transfer 10 of their  {cu(50)} to the volunteer. Practically this means that in this third round the volunteer will earn  {cu(50)}, while the other participants will earn {cu(40)} points. Only the participant who volunteers first will earn the  {cu(50)}; if you decide to volunteer but someone else has volunteered before you, you will earn  {cu(40)} points. Imagine that your small rural community has decided that to access the community centre, residents have to pay a fee, which will be used to compensate the person who prepares the rooms and tidies up afterwards.</p>
        <p>Do you have any questions? If so, please raise your hand virtually. A member of the experimental team will answer your question for everyone.</p>
        <p>The third round will start when everyone in your group has clicked on "Next" the button below, which will redirect you to a new page with the countdown. Again, you can volunteer for your group by clicking on the "Volunteer" button. When you are ready, please click on the "Next" button below. The instructions will remain available at the bottom of the page</p>
        """
        elif player.round_number == 3:
            instructions = """
        <p>Now we will play a fourth round of the game, which will follow exactly the same rules of the third one. The fourth round will start when everyone in your group has clicked on "Next" the button below, which will redirect you to a new page with the countdown. Again, you can volunteer for your group by clicking on the ‘Volunteer’ button. When you are ready, please click on the "Next" button below.</p>
        """
        elif player.round_number == 4:
            # TODO - pull scores from code?
            instructions = f"""
        <p>Now we will play the final round of this game, which will follow exactly the same rules of the first two rounds. The volunteer will have to pay a cost of {cu(50)}, meaning that they will not earn any {units}. If at least one participant volunteers, everyone apart from them will earn {cu(50)}. Only the participant who volunteers first will have to pay the {cu(50)}, and thus overall will not earn any {units}. Anyone who volunteers after them will earn {cu(50)}. If no one volunteers, no one will earn any {units}. Imagine that after some discussions, it was decided in your community to lift the fee for attending the community centre; therefore, the volunteer will not be compensated any more.</p>
        <p>The final round will start when everyone in your group has clicked on "Next" the button below, which will redirect you to a new page with the countdown. Again, you can volunteer for your group by clicking on the "Volunteer" button. When you are ready, please click on the "Next" button below. The instructions will remain available at the bottom of the page.</p>
        """
        elif player.round_number == Constants.num_rounds:
            msg += """
        <p>The game session has finished. Please click on the "Next" button below, and you will be redirected to a short questionnaire, after which you will be communicated your earnings.</p>
        """
        else:
            raise RuntimeError(f"ERROR - unexpected round number {player.round_number}")
        # Record the instructions (for the reminder) or final results text
        if player.round_number == Constants.num_rounds:
            interactive_payoffs = [player.in_round(i+1).payoff for i in range(Constants.num_rounds)]
            participant.volunteer_community_centre_msg = (
                f"In the interactive game, you played {Constants.num_rounds} rounds. "
                f"You earned {interactive_payoffs[0]} in the first round, "
                f"{interactive_payoffs[1]} in the second round, "
                f"{interactive_payoffs[2]} in the third round, "
                f"{interactive_payoffs[3]} in the fourth round, "
                f"and {interactive_payoffs[4]} in the fifth round, "
                f"for a total of <b>{sum(interactive_payoffs)}</b>."
            )
        else:
            participant.volunteer_community_centre_msg = instructions
            msg += instructions
        return {"message": msg}
page_sequence = [Instructions, Understanding, Understood, WaitToStart, Volunteering, Results]