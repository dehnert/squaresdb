"""
Django settings for squaresdb project.

Generated by 'django-admin startproject' using Django 1.8.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True

# EMAIL SETTINGS

DEFAULT_FROM_EMAIL = 'Squares DB <squares-db@mit.edu>'

# Error emails
EMAIL_SUBJECT_PREFIX = '[SquaresDB] '
SERVER_EMAIL = 'squares-db-auto@mit.edu'
ADMINS = [
    ('Squares DB Errors', 'squares-db-errorlog@mit.edu')
]
MANAGERS = ADMINS

# ForcedRecipientEmailBackend sends all email to EMAIL_FORCED_RECIPIENTS,
# rather than the specified recipient. It's useful for testing. Such emails
# are labeled by adding a fake recipient to the "To" header. The label can be
# left the same between dev installs, and an option is defined here:
EMAIL_FORCED_RECIPIENTS_LABEL = "squares-db-forced-recipient@mit.edu"

# AutoBccEmailBackend BCCs specified addresses on all outgoing emails, and is
# intended for production use. We expect to use the following for all prod
# deployments:
EMAIL_AUTO_BCC = ["squares-db-outgoing@mit.edu"]

ENABLE_TESTSHIB = None
from .local import *

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'reversion',
    'social_django',
    'squaresdb.membership',
)

MIDDLEWARE_CLASSES = (
    'reversion.middleware.RevisionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'social_core.backends.open_id.OpenIdAuth',
    #'social_core.backends.google.GoogleOpenId',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.saml.SAMLAuth',
    #'social_core.backends.google.GoogleOAuth',
    #'social_core.backends.twitter.TwitterOAuth',
    #'social_core.backends.yahoo.YahooOpenId',
    'django.contrib.auth.backends.ModelBackend',
)

settings_dir = os.path.dirname(os.path.abspath(__file__))

if os.path.isfile(os.path.join(settings_dir, "saml.key")):
    SOCIAL_AUTH_SAML_SP_ENTITY_ID = "https://tech-squares.mit.edu/"
    SOCIAL_AUTH_SAML_SP_PUBLIC_CERT = open(os.path.join(settings_dir, 'saml.crt')).read()
    SOCIAL_AUTH_SAML_SP_PRIVATE_KEY = open(os.path.join(settings_dir, 'saml.key')).read()
    SOCIAL_AUTH_SAML_ORG_INFO = {
        "en-US": {
            "name": "techsquares",
            "displayname": "MIT Tech Squares",
            "url": "http://tech-squares.mit.edu/"
        }
    }
    SOCIAL_AUTH_SAML_TECHNICAL_CONTACT = {
        "givenName": "Tech Squares",
        "emailAddress": "squares-saml@mit.edu"
    }
    SOCIAL_AUTH_SAML_SUPPORT_CONTACT = {
        "givenName": "Tech Squares",
        "emailAddress": "squares-saml@mit.edu"
    }

    SOCIAL_AUTH_SAML_ENABLED_IDPS = {}

    if ENABLE_TESTSHIB is None: ENABLE_TESTSHIB = DEBUG

    if ENABLE_TESTSHIB:
        SOCIAL_AUTH_SAML_ENABLED_IDPS["testshib"] = {
            "entity_id": "https://idp.testshib.org/idp/shibboleth",
            "url": "https://idp.testshib.org/idp/profile/SAML2/Redirect/SSO",
            # From https://www.testshib.org/metadata/testshib-providers.xml
            "x509cert": open(os.path.join(settings_dir, 'testshib.crt')).read(),
        }

ROOT_URLCONF = 'squaresdb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'squaresdb', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'squaresdb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
