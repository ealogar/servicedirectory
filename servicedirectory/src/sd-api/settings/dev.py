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

DEBUG = True

# ######## MONGO replicaset in development
MONGODB = {'hosts': ('localhost:27017', 'localhost:27018', 'localhost:27019'),
            'dbname': 'sd',
            'slave_ok': True,
            'replicaset_number': 3,
            'replicaset': 'sdrepl',
            'autostart': True
            }
MAX_RETRIES_DAOS = 3

# Run tests with django_nose

INSTALLED_APPS = INSTALLED_APPS + ('django_nose',)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = ['-s',
             '-v',
             '--cover-erase',
             '--cover-branches',
             '--with-cov',
             '--cover-package=classes,commons,users,bindings',
             '--cover-html'
             ]

LOGGING['loggers']['']['level'] = 'DEBUG'
TRACE_EXCEPTIONS = True
