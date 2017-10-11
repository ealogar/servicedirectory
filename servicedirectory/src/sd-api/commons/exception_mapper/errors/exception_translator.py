'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''

# Default exception to be used when no SD exception and no mapping is found
DEFAULT_EXCEPTION = 'GenericServiceError'

EXCEPTIONS = {
    'GenericServiceError': {
        'code': 'SVR1000'
    },
    'UnsupportedMediaType': {
        'code': 'POL0011'
    },
    'NotAcceptable': {
        'code': 'SVC0001'
    },
    # Parse Error is produced when a json input is malformed.
    'ParseError': {
        'code': 'SVC1023'
    },
    'AuthenticationFailed': {
        'code': 'SVC1018'
    },
    'PermissionDenied': {
        'code': 'SVC1013'
    },
    'NotAuthenticated': {
        'code': 'SVC1019'
    },
    'MethodNotAllowed': {
        'code': 'SVC1003'
    }
}
