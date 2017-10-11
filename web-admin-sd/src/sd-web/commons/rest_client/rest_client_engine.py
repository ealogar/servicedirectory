'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
import logging
import re
from restful_lib import Connection
from commons.singleton import Singleton
from commons.rest_client.rest_client_config.sd_config import REQUESTS, GENERAL_PARAMETERS
import base64
from commons.rest_client.exceptions import NotFoundException


logger = logging.getLogger(__name__)


class RestClientEngine(object):

    __metaclass__ = Singleton

    def __init__(self, conn=None):
        if not conn:
            self.conn = Connection(GENERAL_PARAMETERS['base_url'],
                      username=GENERAL_PARAMETERS['username'], password=GENERAL_PARAMETERS['password'])
        else:
            self.conn = conn

    def executeRequest(self, identifier, body=None, query_parameter=None, **kwargs):
        """
        Execute a Http request using pre configured configurations.
        :param identifier Identifier of the configuration block of the request.
        :param body Body content of the request. Default None.
        :param query_parameter Query parameters of URL. apis/apiServ?param1=value1&...  Default None.
        :param kwargs You can include in it pathVariables and extra headers.
        :return Dictionary with the body response and headers that contains status code too.
        :raises NotFoundException if a parameter is not present in config or in method call.
        """
        rel_url = self.buildUrl(identifier, kwargs)
        headers = self.buildHeaders(identifier, kwargs)

        if identifier in REQUESTS:
            if REQUESTS[identifier]['method'] in ('get', 'post', 'put', 'delete'):
                if REQUESTS[identifier]['method'] == 'get':
                    return self.conn.request_get(rel_url, headers=headers, args=query_parameter)
                elif REQUESTS[identifier]['method'] == 'post':
                    return self.conn.request_post(rel_url, headers=headers, body=body)
                elif REQUESTS[identifier]['method'] == 'put':
                    return self.conn.request_put(rel_url, headers=headers, body=body)
                elif REQUESTS[identifier]['method'] == 'delete':
                    return self.conn.request_delete(rel_url, headers=headers)
                else:
                    raise NotFoundException('method not found')
            else:
                raise NotFoundException('method not found')

    def buildHeaders(self, identifier, kwargs):
        result = {}
        if 'headers' in GENERAL_PARAMETERS:
            for key, value in GENERAL_PARAMETERS['headers'].items():
                result[key] = value

        if identifier in REQUESTS:
            if 'headers' in REQUESTS[identifier]:
                for key, value in REQUESTS[identifier]['headers'].items():
                    result[key] = value
        else:
            raise NotFoundException('Request identifier not found exception.')

        if 'headers' in kwargs:
            for key, value in kwargs['headers'].items():
                result[key] = value

        if GENERAL_PARAMETERS['username'] and GENERAL_PARAMETERS['password']:
            result['Authorization'] = ''.join(['Basic ',
                                               base64.b64encode(':'.join([GENERAL_PARAMETERS['username'],
                                                                          GENERAL_PARAMETERS['password']]))])

        return result

    def buildUrl(self, identifier, kwargs):
        if identifier in REQUESTS:
            relative_url = REQUESTS[identifier]['relative_url']
        else:
            raise NotFoundException('Request identifier not found exception.')

        parameters = self.getParameterFromConfigFile(relative_url)

        replaced_relative_url = self.replaceParameters(relative_url, parameters, kwargs)

        return replaced_relative_url

    def getParameterFromConfigFile(self, relative_url):
        return re.findall('{(?P<parameter>[a-zA-Z%0-9_-]+)}', relative_url)

    def replaceParameters(self, relative_url, parameters, kwargs):
        result = relative_url
        for parameter in parameters:
            if parameter in kwargs:
                result = result.replace(''.join(['{', parameter, '}']), kwargs[parameter], 1)
            else:
                raise NotFoundException(''.join(['Parameter ', parameter, ' not found for build the url']))
        return result
