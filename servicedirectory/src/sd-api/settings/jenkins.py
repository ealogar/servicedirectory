'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
from common import *

# ######## MONGO standalone configuration in development
MONGODB = {'hosts': ('localhost:27017',),
            'dbname': 'sd',
            'slave_ok': True,
            'replicaset_number': 1,  # although is not a replicaset, we use value for testing
            'replicaset': '',
            'autostart': True
            }
MAX_RETRIES_DAOS = 3

# Override loggers to use console for jenkins
# Override loggers to use console for jenkins
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'ERROR',
        },
        'django.db': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
            }
    }
}
INSTALLED_APPS = INSTALLED_APPS + ('django_nose', )

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = ['-s',
             '-v',
             '--cover-erase',
             '--cover-branches',
             '--with-cov',
             '--cover-package=classes,commons,users,bindings',
             '--cover-xml',
             '--cover-xml-file=target/site/cobertura/coverage.xml',
             '--with-xunit',
             '--xunit-file=target/surefire-reports/TEST-nosetests.xml'
             ]
