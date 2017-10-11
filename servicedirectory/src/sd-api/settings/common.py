'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
from os.path import abspath, dirname, join, normpath

# Django settings for ebooks project.
DJANGO_ROOT = dirname(dirname(abspath(__file__)))
DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

MONGODB = {'hosts': ('localhost:27017',),
           'dbname': 'sd',
           'slave_ok': True,
           'replicaset_number': 1,
           'replicaset': '',
           'autostart': True
           }

# Config params for daos using mongodb
# This param set which dao functions will be retried if a mongo operation fails
RETRY_FUNCTIONS_DAOS = (u'^get', u'^find', u'^update', u'^delete')
# The sleep time in milliseconds to wait after retry dao operation
DELAY_OP_DAOS = 3500
# The multiply factor for delay between retries
BACKOFF_OP_DAOS = 1.1
# maximun retries in daos when connection is lost
MAX_RETRIES_DAOS = 2

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # default database, just for testing purposes if needed
        'NAME':  normpath(join(DJANGO_ROOT, 'sd.db')),      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    normpath(join(DJANGO_ROOT, 'static', 'rest_framework')),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '54#7do4hw1g61^$khv+lw2it5p5gn&ky(ql11dk4vpy9c-z0y4'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'commons.middleware.OperationTypeMiddleware',
    'commons.middleware.TransactionIdMiddleware',
    'commons.middleware.UnicaCorrelatorMiddleware',
    'django.middleware.common.CommonMiddleware'
)

# This should point to urls entry point
ROOT_URLCONF = 'urls'

# In mac this line should be overriden if not using wsgi
# WSGI_APPLICATION = 'books.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'classes',
    'users',
    'bindings',
    'rest_framework'
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        # Define here the filters for add extra args to logger, don't forget to add filters in handlers...
        'transaction_id': {
            '()': 'commons.logger.TransactionIDFilter'
        },
        'correlator_id': {
            '()': 'commons.logger.CorrelatorIDFilter'
        },
        'op_type': {
            '()': 'commons.logger.OpTypeFilter'
        },
        'tdaf_levelname': {
            '()': 'commons.logger.LevelNameFilter'
        }
    },
    'formatters': {
        'verbose': {
            'format': 'time=%(asctime)s.%(msecs)03dZ | lvl=%(tdaf_levelname)s | corr=%(correlator_id)s | trans=%(transaction_id)s | op=%(op_type)s | msg=%(module)s: %(message)s',
            'datefmt': '%Y-%m-%dT%H:%M:%S',  # specify formatter as miliseconds are separated by comma by default
            'converter': 'time.gmtime'  # use UTC time (formerly known as gmt)
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
         'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/log/servdir/sd.log',
            'formatter': 'verbose',
            'filters': ['transaction_id', 'correlator_id', 'op_type', 'tdaf_levelname']
        }
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'INFO',
            }
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'users.authentication.BasicMongoAuthentication',
        ),
    'DEFAULT_PARSER_CLASSES': (
        'commons.parsers.JSONStrictParser',  # We use our parser to launch exception in duplicated keys
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    )
}

# Do not leave django append slash if a url don't provide slash at the end
# Redirect when put methods become a GET
APPEND_SLASH = False

JSON_SCHEMAS_FOLDER = normpath(join(DJANGO_ROOT, 'schemas'))

# Defines the user credentials to use Service directory (default user)
SD_USERNAME = 'admin'
SD_PASSWORD = 'admin'

# Defines the query parameter in searches to define the expected return fields in response
# e.g. : filters=field1,field2
REQUEST_FILTER_PARAM = 'filters'

# Set the allowed characters in class_name (url mapping and validations)
ALPHANUMERIC_REGEX = '[a-zA-Z0-9_-]+'
CLASS_NAME_REGEX = ALPHANUMERIC_REGEX
USER_NAME_REGEX = ALPHANUMERIC_REGEX
ORIGIN_REGEX = '^{0}$'.format(ALPHANUMERIC_REGEX)

# Allowed characters for the attributes dynamic keys when defining instances
ATTTRIBUTES_KEYS_REGEX = '[a-z0-9_-]+'

# Allowed characters for the input_contex_param keys when defining rules
INPUT_CONTEXT_KEYS_CREATE_REGEX = '(?!^class_name$|^origin$)(^[a-z0-9_-]+$)'
# Allowed characters for querying input_contex_params and aditional query params
INPUT_CONTEXT_KEYS_REGEX = '^[a-z0-9_-]+$'
QUERY_PARAMS_GET_ENDPOINTS = '^version$|^environment$|^filters$|^attributes.[a-z0-9_-]+$'
QUERY_PARAMS_GET_BINDINGS = '^class_name$|^origin$'


# Automatic loggin configuration
# Define which layer we want to automatically log methods
LOG_LAYERS = ('services', 'daos')
# Define here the default log method wich will be used (debug, info, warning, error)
DEFAULT_LOG_METHOD = 'debug'
# Defining LOG_METHOD_SERVICES we override default log method defined uper
# You can also define aditional layers methods using the name LOG_METHOD_<LAYER> like LOG_METHOD_DAOS
LOG_METHOD_SERVICES = 'info'

# Service directory names
APP_NAME = 'Service Directory'
VERSION = 'v1'

# In django 1.5 allowed_host has been introduced as a new security measure
ALLOWED_HOSTS = ['*']

# Custom header for unica correlator id
UNICA_CORRELATOR_REQUEST_HEADER = 'HTTP_UNICA_CORRELATOR'
UNICA_CORRELATOR_RESPONSE_HEADER = 'Unica-Correlator'

# Set to True to print excpetion traceback when handling_exceptions
TRACE_EXCEPTIONS = False
