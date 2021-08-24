from os import environ
SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=0.05, participation_fee=5)
SESSION_CONFIGS = [dict(name='complete_session', num_demo_participants=12, app_sequence=['risk_attitude', 'volunteering', 'questionnaire_and_payment']), dict(name='just_volunteering', num_demo_participants=12, app_sequence=['volunteering'])]
LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'GBP'
USE_POINTS = True
DEMO_PAGE_INTRO_HTML = ''
PARTICIPANT_FIELDS = ['risk_attitude_msg', 'volunteering_msg', 'volunteering_framing']
SESSION_FIELDS = []
ROOMS = []

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

SECRET_KEY = 'blahblah'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']


DEMO_PAGE_INTRO_HTML = 'Risk attitude lottery game based on Holt and Laury (2002), followed by an interactive multi-player game about volunteering. <a href="https://github.com/peterjc/MDT-INTR-EXP-MET">Source code on GitHub</a>.'
