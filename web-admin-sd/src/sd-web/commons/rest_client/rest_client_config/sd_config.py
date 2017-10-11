'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''

GENERAL_PARAMETERS = {
    'headers': {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'User-Agent': 'SD-Web'
    },
    'base_url': 'http://localhost:8000/sd/v1',
    'username': 'admin',
    'password': 'admin'
}

REQUESTS = {
    'getEndpoints': {
        'relative_url': 'apis/{api_name}/endpoints',
        'headers': {
            'Custom-Header': 'My Custom Header'
        },
        'method': 'get'
    },
    'getCapabilities': {
        'relative_url': 'apis',
        'headers': {
            'Custom-Header': 'My Custom Header'
        },
        'method': 'get'
    },
    'createCapability': {
        'relative_url': 'apis',
        'headers': {
            'Custom-Header': 'My Custom Header'
        },
        'method': 'post'
    },
    'removeCapability': {
        'relative_url': 'apis/{api_name}',
        'method': 'delete'
    },
    'modifyCapability': {
        'relative_url': 'apis/{api_name}',
        'method': 'post'
    },
    'addEndpoint': {
        'relative_url': 'apis/{api_name}/endpoints',
        'method': 'post'
    },
    'modifyEndpoint': {
        'relative_url': 'apis/{api_name}/endpoints/{id_end}',
        'method': 'put'
    },
    'removeEndpoint': {
        'relative_url': 'apis/{api_name}/endpoints/{id_end}',
        'method': 'delete'
    }
}
