# Configuration settings for the AI recruitment system

DATABASE_URI = 'sqlite:///ai_recruitment.db'
LOG_LEVEL = 'INFO'
MAX_CANDIDATES_TO_SHORTLIST = 50
INTERVIEW_SLOT_DURATION = 30  # in minutes
EMAIL_TEMPLATE_PATH = 'templates/email_invitation.html'
DIVERSITY_INCLUSION_ENABLED = True
MATCH_SCORE_THRESHOLD = 80  # percentage for automatic shortlisting
