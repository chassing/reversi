""" Production settings and globals.
"""


from os import environ

from base import *

# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.
from django.core.exceptions import ImproperlyConfigured


def get_env_setting(setting):
    """ Get the environment setting or return exception """
    try:
        return environ[setting]
    except KeyError:
        error_msg = "Set the %s env variable" % setting
        raise ImproperlyConfigured(error_msg)

INSTALLED_APPS += (
    'gunicorn',
    'storages',
)

########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = get_env_setting('SENDGRID_SMTP')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-password
EMAIL_HOST_PASSWORD = get_env_setting('SENDGRID_PASSWORD')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-user
EMAIL_HOST_USER = get_env_setting('SENDGRID_USERNAME')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = 587

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = '[%s] ' % SITE_NAME

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-use-tls
EMAIL_USE_TLS = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = EMAIL_HOST_USER
########## END EMAIL CONFIGURATION


########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = get_env_setting('SECRET_KEY')
########## END SECRET CONFIGURATION


########## STATIC FILE CONFIGURATION
# Production storage using s3.
DEFAULT_FILE_STORAGE = 's3storages.MediaStorage'
STATICFILES_STORAGE = 's3storages.StaticStorage'
STATIC_URL = 'https://se2reversi.s3.amazonaws.com/static/'
ADMIN_MEDIA_PREFIX = 'https://se2reversi.s3.amazonaws.com/static/admin/'
MEDIA_URL = 'https://se2reversi.s3.amazonaws.com/media/'

AWS_QUERYSTRING_AUTH = False
########## END STATIC FILE CONFIGURATION

LOGGING["loggers"]["main"]["level"] = "INFO"
LOGGING["loggers"]["sockets"]["level"] = "INFO"


ALLOWED_HOSTS = [
    "reversi.ca-net.org",
    "still-dusk-5467.herokuapp.com",
]


# needed for cached static files
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake'
    }
}
