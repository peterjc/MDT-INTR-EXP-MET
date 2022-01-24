
from otree.api import *
c = cu

doc = 'Multi-round volunteer dilemma with treatment specific framing (e.g. community centre).'
class C(BaseConstants):
    NAME_IN_URL = 'volunteering'
    PLAYERS_PER_GROUP = 6
    NUM_ROUNDS = 5
    VOLUNTEER_TIMEOUT = 15
class Subsession(BaseSubsession):
    start_timestamp = models.FloatField()
def record_round_start(subsession: Subsession):
    session = subsession.session
    import time
    subsession.start_timestamp = time.time()
class Group(BaseGroup):
    pass
class Player(BasePlayer):
    volunteer = models.BooleanField(choices=[[True, 'Yes'], [False, 'No']], initial=False, label='Do you volunteer?')
    submission_timestamp = models.FloatField()
    understanding1 = models.IntegerField(label='No one in your group volunteers within the time available. How many points will you earn?', min=0)
    understanding2 = models.IntegerField(label='You volunteer but someone else has volunteered before you. How many points will you earn? ', min=0)
    understanding3 = models.IntegerField(label='How many points will you earn if you volunteer first?', min=0)
def understanding1_error_message(player: Player, value):
    group = player.group
    if value != 0:
        return f"Actually, if no one in the group volunteers all of you earn {cu(0)}."
def understanding2_error_message(player: Player, value):
    if value != 50:
        return f"Actually, if someone volunteers before you, they  earn {cu(0)}, but you still earn {cu(50)}."
def understanding3_error_message(player: Player, value):
    if value != 0:
        return f"Actually, if you are the first person to volunteer, you earn {cu(0)}."
class WaitAndGroup(WaitPage):
    wait_for_all_groups = True
    title_text = 'Waiting for other players to begin'
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
class Instructions(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    @staticmethod
    def vars_for_template(player: Player):
        session = player.session
        group = player.group
        participant = player.participant
        from otree.settings import POINTS_CUSTOM_NAME
        units = POINTS_CUSTOM_NAME if POINTS_CUSTOM_NAME else "points"
        volunteering_framing = bool(session.config.get('framing', 0))
        if volunteering_framing:
            # framing=1 gives True, Community Centre
            framing_msg = f"""
        <p>
        Imagine that the {C.PLAYERS_PER_GROUP} people in your group reside in the same small rural community. In your community there is a community centre where people can meet during the day to have a coffee or tea together and do a series of activities. All the residents have access to the centre but in order to enjoy this space, someone must open it and prepare the rooms as well as tidy up and clean afterwards. If no one volunteers to do this, the centre remains closed. The activities implemented in the centre benefit all residents attending.  This benefit has a value of {cu(50)}. The volunteer incurs personal costs in terms of time and energy are also worth {cu(50)}, which means that they are left with {cu(0)}.
        </p>
        """
        else:
            # framing=0 gives False, farmers
            framing_msg = f"""
        <p>
        Imagine that the {C.PLAYERS_PER_GROUP} people in your group are farmers located next to a river on a catchment area subject to regular flooding that affects them all. To prevent flooding, a flood expansion plain could be created on one of the {C.PLAYERS_PER_GROUP} farmers’ fields. This would mean that 1 farmer would lose the production from the field converted into a flood expansion plain. This loss has a value of {cu(50)} in the game. If the flood expansion plain is created, all {C.PLAYERS_PER_GROUP} farmers would be protected from floods, would avoid the costs associated with floods, and would save the equivalent of {cu(50)} each. This means that the farmer who volunteers will be left with {cu(0)}, and the {C.PLAYERS_PER_GROUP - 1} other farmers with {cu(50)} each at the end of the round.
        </p>
        """
        if player.round_number == 1:
            msg = f"""
        <p>
        Thank you for playing the first game. Now we will play a second game.
        </p>
        <p>
        This game consists of {C.NUM_ROUNDS} rounds. In each round, you will receive instructions and will be asked to make a decision. The decisions in each round are completely independent from each other. Your earnings from each round will depend on your decision, as well as the decisions that other participants make in that round.
        </p>
        <p>
        The computer will group you with other {C.PLAYERS_PER_GROUP - 1} participants, making a group of {C.PLAYERS_PER_GROUP}. The group will remain the same during the {C.NUM_ROUNDS} rounds.
        </p>
        <p>
        In each round, each of the members of your group has the opportunity to earn {cu(50)}. In order for the members of your group to earn the {cu(50)}, at least one of you needs to ‘volunteer’.
        </p>
        <p>
        The volunteer will have to pay a cost of {cu(50)}, meaning that they will not earn any {units} in that round. You will have {C.VOLUNTEER_TIMEOUT} seconds to decide whether to volunteer.
        </p>
        <p>
        If at least one participant in your group volunteers, everyone apart from them will earn {cu(50)}. Only the participant who volunteers first will have to pay the {cu(50)}, and thus will not earn any {units}. Those who will possibly volunteer after them will  not be considered as volunteers and will thus receive {cu(50)}.
        </p>
        <p>
        If no one volunteers, no one will earn any {units}. At the end of the {C.VOLUNTEER_TIMEOUT} seconds, you will be automatically redirected to the page with the results of that round. You will be told whether anyone has volunteered, and your total earnings in that round. You will not know the identity of the person who has volunteered.
        </p>
        {framing_msg}
        <p>
        To summarise, there are 3 options:
        <ol>
        <li>You volunteer first in your group: you earn {cu(0)}, and the {C.PLAYERS_PER_GROUP-1} other participants earn {cu(50)} each.</li>
        <li>You volunteer but someone else volunteers first in your group: you and {C.PLAYERS_PER_GROUP-2} other participants earn {cu(50)} while 1 other participant who volunteered first earns {cu(0)}.</li>
        <li>None of the {C.PLAYERS_PER_GROUP} participants in your group volunteers: you and the other 5 participants each receive {cu(0)}.</li>
        </ol>
        </p>
        <p>
        Do you have any questions? If so, please ask the <i>Host</i> using the video conference chat function, and the experimenter will answer your question for everyone.
        </p>
        <p>
        Now please click ‘Next’, and you will be redirected to a page with questions to check your understanding of the instructions.
        </p>
        """
        else:
            msg = f"ERROR - Invalid round number {player.round_number}"
        return {"instructions": msg}
class Understanding(Page):
    form_model = 'player'
    form_fields = ['understanding1', 'understanding2', 'understanding3']
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
class Understood(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
class WaitToStart(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = record_round_start
    title_text = 'Waiting for other players to begin'
class Volunteering(Page):
    form_model = 'player'
    form_fields = ['volunteer']
    timer_text = 'You have 15 seconds to decide.'
    @staticmethod
    def is_displayed(player: Player):
        session = player.session
        subsession = player.subsession
        # Expecting will always be (just under) 15s left,
        import time
        return C.VOLUNTEER_TIMEOUT - time.time() + subsession.start_timestamp > 1
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        if player.round_number in [1, 2, 5]:
            # Self-less volunteer:
            instructions = f"<p>To volunteer you need to click the button before the end of the {C.VOLUNTEER_TIMEOUT} seconds. If no one in your group volunteers, all of you earn {cu(0)}. If at least one person volunteers, the first person who volunteers earns {cu(0)} and the other {C.PLAYERS_PER_GROUP-1} members of the group earn {cu(50)}. At the end of the {C.VOLUNTEER_TIMEOUT} seconds, you will be automatically redirected to the page with the results of this round.</p>"
        else:
            # Compensated volunteer:
            instructions = f"<p>To volunteer you need to click the button before the end of the {C.VOLUNTEER_TIMEOUT} seconds. If no one in your group volunteers, all of you earn {cu(0)}. If at least one person volunteers, the first person who volunteers earns 50 points and the other {C.PLAYERS_PER_GROUP-1} members of the group earn {cu(40)}. At the end of the {C.VOLUNTEER_TIMEOUT} seconds, you will be automatically redirected to the page with the results of this round.</p>"
        return {"instructions": instructions}
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        session = player.session
        subsession = player.subsession
        import time  # hack, want this at top level really
        # Convert to a relative timestamp (in seconds):
        player.submission_timestamp = time.time() - subsession.start_timestamp
    @staticmethod
    def get_timeout_seconds(player: Player):
        session = player.session
        subsession = player.subsession
        import time
        return C.VOLUNTEER_TIMEOUT - time.time() + subsession.start_timestamp
class Results(Page):
    form_model = 'player'
    @staticmethod
    def vars_for_template(player: Player):
        session = player.session
        group = player.group
        participant = player.participant
        from otree.settings import POINTS_CUSTOM_NAME
        units = POINTS_CUSTOM_NAME if POINTS_CUSTOM_NAME else "points"
        volunteering_framing = bool(session.config.get('framing', 0))
        # Rules and payoff depend on round...
        # See also the instructions reminder on the Volunteering page
        msg = "<p>Thanks for making your choice.</p>"
        # Was this player first to volunteer in their group?
        players = group.get_players()
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
            msg += """
        <p>Now we will play a second round of the game, which will follow exactly the same rules as the first one. The second round will start when everyone in your group has clicked on the ‘Next’ button below, which will redirect you to a new page with the countdown. Again, you can volunteer for your group by clicking on the ‘Volunteer’ button. When you are ready, please click on the ‘Next’ button below.</p>
        """
        elif player.round_number == 2:
            # TODO - pull scores from code? Tricky as this is about the NEXT round
            if volunteering_framing:
                framing_msg = "Imagine that your small rural community has decided that to access the community centre, residents have to pay a fee, which will be used to compensate the person who prepares the rooms and tidies up afterwards."
            else:
                framing_msg = "Imagine that the group of farmers has decided to compensate the volunteering farmer for the provision of the flood protection service provided to the catchment."
            msg += f"""
        <p>Now we will play a third round of the game, which will follow slightly different rules. Again, at least one person in your group needs to volunteer in order for you to earn some {units}, meaning that if no one volunteers, no one will earn any {units}. As previously, if there is a volunteer, all other participants benefit by {cu(50)}. However, in this round, all other participants will transfer 10 of their {cu(50)} to the volunteer. Practically this means that in this third round the volunteer will earn {cu(50)}, while the other participants will earn {cu(40)} each. Only the participant who volunteers first will earn {cu(50)}; if you decide to volunteer but someone else has volunteered before you, you will earn {cu(40)}.</p>
        <p>{framing_msg}</p>
        <p>
        To summarise, there are 3 options:
        <ol>
        <li>You volunteer first in your group: you earn {cu(50)}, and the {C.PLAYERS_PER_GROUP-1} other participants earn {cu(40)} each.</li>
        <li>You volunteer but someone else volunteers first in your group: you and {C.PLAYERS_PER_GROUP-2} other participants earn {cu(40)} while 1 other participant who volunteered first earns {cu(50)}.</li>
        <li>None of the {C.PLAYERS_PER_GROUP} participants in your group volunteers: you and the other 5 participants each receive {cu(0)}.</li>
        </ol>
        </p>
        <p>Do you have any questions? If so, please ask the <i>Host</i> using the video conference chat function, and the experimenter will answer your question for everyone.</p>
        <p>The third round will start when everyone in your group has clicked on the ‘Next’ button below, which will redirect you to a new page with the countdown. Again, you can volunteer for your group by clicking on the ‘Volunteer’ button. When you are ready, please click on the ‘Next’ button below. The instructions will remain available at the bottom of the page.</p>
        """
        elif player.round_number == 3:
            msg += """
        <p>Now we will play a fourth round of the game, which will follow exactly the same rules of the third one. The fourth round will start when everyone in your group has clicked on the ‘Next’ button below, which will redirect you to a new page with the countdown. Again, you can volunteer for your group by clicking on the ‘Volunteer’ button. When you are ready, please click on the ‘Next’ button below.</p>
        """
        elif player.round_number == 4:
            # TODO - pull scores from code?
            if volunteering_framing:
                framing_msg = "Imagine that after some discussions, it was decided in your community to lift the fee for attending the community centre; therefore, the volunteer will not be compensated any more."
            else:
                framing_msg = "Imagine that after some discussions, it was decided in the catchment to lift the compensation scheme for the farmer who volunteers; therefore, the volunteer will not be compensated any more."
            msg += f"""
        <p>Now we will play the final round of this game, which will follow exactly the same rules as the first two rounds.<p>
        <p>{framing_msg}</p>
        <p>The volunteer will have to pay a cost of {cu(50)}, meaning that they will not earn any {units}. If at least one participant volunteers, everyone will earn {cu(50)}. Only the participant who volunteers first will have to pay the {cu(50)}, and thus overall will not earn any {units}. Anyone who volunteers after them will earn {cu(50)} overall. If no one volunteers, no one will earn any {units}.</p>
        <p>The final round will start when everyone in your group has clicked on the ‘Next’ button below, which will redirect you to a new page with the countdown. Again, you can volunteer for your group by clicking on the ‘Volunteer’ button. When you are ready, please click on the ‘Next’ button below. The instructions will remain available at the bottom of the page.</p>
        """
        elif player.round_number == C.NUM_ROUNDS:
            msg += """
        <p>The game session has finished. Please click on the ‘Next’ button below, and you will be redirected to a short questionnaire, after which you will be communicated your earnings.</p>
        """
        else:
            raise RuntimeError(f"ERROR - unexpected round number {player.round_number}")
        # Record final results text via participant field:
        if player.round_number == C.NUM_ROUNDS:
            interactive_payoffs = [player.in_round(i+1).payoff for i in range(C.NUM_ROUNDS)]
            participant.volunteering_msg = (
                f"In the interactive game, you played {C.NUM_ROUNDS} rounds. "
                f"You earned {interactive_payoffs[0]} in the first round, "
                f"{interactive_payoffs[1]} in the second round, "
                f"{interactive_payoffs[2]} in the third round, "
                f"{interactive_payoffs[3]} in the fourth round, "
                f"and {interactive_payoffs[4]} in the fifth round, "
                f"for a total of <b>{sum(interactive_payoffs)}</b>."
            )
        return {"message": msg}
page_sequence = [WaitAndGroup, Instructions, Understanding, Understood, WaitToStart, Volunteering, Results]