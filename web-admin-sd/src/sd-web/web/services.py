'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
import json
import logging
from commons.rest_client.rest_client_engine import RestClientEngine
from commons.singleton import Singleton

logger = logging.getLogger(__name__)


class BaseService(object):
    __metaclass__ = Singleton


class CapabilitiesService(BaseService):

    def __init__(self):
        self.rest_client = RestClientEngine()

    def create_capability(self, capability_element):
        result = self.rest_client.executeRequest('createCapability', body=json.dumps(capability_element))
        if result['headers']['status'] == '201':
            logger.debug(' '.join(['Capability', capability_element['api_name'], 'created.']),)
            return {'result': 'Capability Created'}
        else:
            logger.debug(' '.join(['Capability', capability_element['api_name'], 'creation failed.']),)
            return result

    def remove_capability(self, capability):
        result = self.rest_client.executeRequest('removeCapability', api_name=capability)
        if result['headers']['status'] == '204':
            logger.debug(' '.join(['Capability', capability, 'removed.']),)
            return {'result': 'Capability Removed'}
        else:
            logger.debug(' '.join(['Capability', capability, 'deletion failed.']),)
            return result

    def modify_capability(self, capability_element):
        api_name = capability_element.pop('api_name', None)

        result = self.rest_client.executeRequest('modifyCapability', api_name=api_name,
                                                 body=json.dumps(capability_element))
        if result['headers']['status'] == '200':
            logger.debug(' '.join(['Capability', api_name, 'updated.']),)
            return {'result': 'Capability Updated'}
        else:
            logger.debug(' '.join(['Capability', api_name, 'updated failed.']),)
            return result

    def get_capabilities(self):
        result = self.rest_client.executeRequest('getCapabilities')
        if result['headers']['status'] == '200':
            logger.debug('Capabilities retrieve successfully.')
            return json.loads(result['body'])
        else:
            logger.debug('Failure retrieving capabilities.')
            return result


class EndpointsService(BaseService):

    def __init__(self):
        self.rest_client = RestClientEngine()

    def get_endpoints(self, api_name):
        result = self.rest_client.executeRequest('getEndpoints', api_name=api_name)
        if result['headers']['status'] == '200':
            logger.debug(''.join(['Endpoints of capability ', api_name, ' retrieve successfully.']),)
            return json.loads(result['body'])
        else:
            logger.debug(''.join(['Failure retrieving endpoints from ', api_name, '.']),)
            return result

    def addEndpoint(self, data):
        api_name = data.pop('api_name', None)
        if len(data['ob']) == 0:
            data.pop('ob', None)
        body = json.dumps(data)
        result = self.rest_client.executeRequest('addEndpoint', api_name=api_name, body=body)
        if result['headers']['status'] == '201':
            logger.debug(''.join(['Added endpoint to ', api_name, ' successfully.']),)
            return json.loads(result['body'])
        else:
            logger.debug(''.join(['Failure adding endpoint to ', api_name, '.']),)
            return result

    def modifyEndpoint(self, data):
        api_name = data.pop('api_name', None)
        id_end = data.pop('id_end', None)
        if len(data['ob']) == 0:
            data.pop('ob', None)
        body = json.dumps(data)
        result = self.rest_client.executeRequest('modifyEndpoint', api_name=api_name, id_end=id_end, body=body)
        if result['headers']['status'] == '200':
            logger.debug(''.join(['Endpoint ', id_end, ' updated successfully.']),)
            return json.loads(result['body'])
        else:
            logger.debug(''.join(['Failure updating endpoint ', id_end, '.']),)
            return result

    def removeEndpoint(self, data):
        api_name = data.pop('api_name', None)
        id_end = data.pop('id_end', None)
        result = self.rest_client.executeRequest('removeEndpoint', api_name=api_name, id_end=id_end)
        if result['headers']['status'] == '204':
            logger.debug(''.join(['Endpoint ', id_end, ' removed successfully.']),)
            return {'result': 'Endpoint removed'}
        else:
            logger.debug(''.join(['Failure removing endpoint ', id_end, '.']),)
            return result
