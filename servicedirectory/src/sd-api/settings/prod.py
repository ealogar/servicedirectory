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

DEBUG = False

# Sample prod.py configuration file, you should uncomment the different options according to your needs

# ######## MONGO replicaset in development, example, uncomment and change
#MONGODB = {'hosts': ('localhost:27017', 'localhost:27018', 'localhost:27018',),
#           'dbname': 'sd',
#           'slave_ok': True,
#           'replicaset_number': 3,
#           'replicaset': '',
#           'autostart': True
#           }

# Defines the user credentials to use Service directory (default user)
SD_USERNAME = 'admin'
SD_PASSWORD = 'admin'

# Service directory log levels in production
LOGGING['loggers']['']['level'] = 'INFO'

# only accept json (avoid CSS with rest framework templates)
#REST_FRAMEWORK['DEFAULT_PARSER_CLASSES'] = ('commons.parsers.JSONStrictParser',)

# we only return json (avoid CSS with rest framework templates)
#REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = ('rest_framework.renderers.JSONRenderer',)

# append middleware to handle https secure access (uncomment to only allow http access to bind_instances and info)
#MIDDLEWARE_CLASSES = ('commons.middleware.MultipleProxyMiddleware',
#                      'commons.middleware.SSLRedirectMiddleware') \
#                    + MIDDLEWARE_CLASSES
