'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
from __future__ import unicode_literals  # Make all strings in file converted to unicode

ERRORS = {
    'SVR1000': {
        'details': 'Generic Server Error: {0}',
        'status_code': 500
    },
    'SVC1006': {
        'details': 'Resource {0} does not exist',
        'status_code': 404
    },
    'SVC1021': {
        'details': 'Invalid parameter value: {0}. Supported values are: {1}',
        'status_code': 400
    },
    'SVC1000': {
        'details': 'Missing mandatory parameter: {0}',
        'status_code': 400
    },
    'SVC1024': {
        'details': 'Repeated query parameter: {0}',
        'status_code': 400
    },
    'SVC1001': {
        'details': 'Invalid parameter: {0}',
        'status_code': 400
    },
    'SVC0001': {
        'details': 'Generic Client Error: {0}',
        'status_code': 400
    },
    'SVC0002': {
        'details': 'Invalid parameter value: {0}',
        'status_code': 400
    },
    'SVC0003': {
        'details': 'Invalid parameter value: {0}. Possible values are: {1}',
        'status_code': 400
    },
    'SVC1023': {
        'details': 'Parser Error: JSON content not well formed',
        'status_code': 400
    },
    'SVC1018': {
        'details': 'Invalid Credentials',
        'status_code': 401
    },
    'SVC1013': {
        'details': '{0} Operation is not allowed: invalid-permissions',
        'status_code': 403
    },
    'SVC1019': {
        'details': 'Application cannot use API/Feature',
        'status_code': 403
    },
    'SVC1003': {
        'details': 'Requested Operation does not exist: {0}',
        'status_code': 405
    },  # Service directory errors inside UNICA expecification
    'POL0011': {
        'details': 'Media type {0} not supported',
        'status_code': 403
    },
    'SVC2002': {
        'details': 'Binding resource {0} does not exist',
        'status_code': 404
    },
    'SVC2003': {
        'details': 'Resource {0} has been deleted',
        'status_code': 404
    },
    # error with empty details means no body in response...
    'SVC0001': {
        'details': None,
        'status_code': 406
    }
}
