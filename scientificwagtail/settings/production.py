from .base import *


DEBUG = False

# Postgresql search backend
INSTALLED_APPS = INSTALLED_APPS + [
    'wagtail.contrib.postgres_search',
]

WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.contrib.postgres_search.backend',
        'SEARCH_CONFIG': 'english',
    },
}   

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

ALLOWED_HOSTS = ['example.com']

EMAIL_SUBJECT_PREFIX = '[Scientific Wagtail] '

ADMINS = [
    # ('Admin name', 'admin_email@example.com'),
]

MANAGERS = ADMINS

# Logging is configured to send emails to administrators
# when 5XX errors occur
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

try:
    from .local import *
except ImportError:
    pass
