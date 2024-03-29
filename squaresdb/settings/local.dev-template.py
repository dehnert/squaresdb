import os

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = something

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

EMAIL_BACKEND = 'squaresdb.utils.email.ForcedRecipientEmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_FORCED_RECIPIENTS = ['squares-db-forced-recipient@mit.edu']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)-8s %(name)-15s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'squaresdb': {
            'handlers': ['console'],
            'level': os.getenv('SQUARESDB_LOG_LEVEL', 'INFO'),
        },
    },
}
