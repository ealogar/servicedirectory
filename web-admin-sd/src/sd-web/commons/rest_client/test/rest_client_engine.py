'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
import unittest
from mock import patch, MagicMock

from commons.rest_client.rest_client_engine import RestClientEngine
from commons.rest_client.exceptions import NotFoundException


class RestClientEngineTest(unittest.TestCase):

    GENERAL_PARAMETERS = {
        'headers': {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': 'SD-Web'
        },
        'base_url': 'http://localhost:8000/sd/v1',
        'username': None,
        'password': None
    }

    REQUESTS = {
        'sampleEndpoint1': {
            'relative_url': 'apis/{api_name}/endpoints',
            'method': 'get'
        },
        'sampleEndpoint2': {
            'relative_url': 'apis',
            'headers': {
                'Custom-Header': 'My Custom Header'
            },
            'method': 'post'
        },
        'sampleEndpoint3': {
            'relative_url': 'apis/{api_name}/{id}',
            'headers': {
                'Custom-Header': 'My Custom Header'
            },
            'method': 'put'
        },
        'sampleEndpoint4': {
            'relative_url': 'apis',
            'method': 'delete'
        },
        'sampleEndpoint5': {
            'relative_url': 'apis',
            'method': 'invented'
        }
    }

    conn = MagicMock(name='ConnectionMock')

    rest_client_engine = None

    def setUp(self):
        self.rest_client_engine = RestClientEngine(self.conn)

    def test_rest_client_engine_should_be_a_singleton(self):
        rest_client = RestClientEngine(self.conn)
        self.assertEquals(id(self.rest_client_engine), id(rest_client))

    @patch('commons.rest_client.rest_client_engine.GENERAL_PARAMETERS', GENERAL_PARAMETERS)
    @patch('commons.rest_client.rest_client_engine.REQUESTS', REQUESTS)
    def test_rest_client_sample1_should_perform_get_request(self):
        self.rest_client_engine.executeRequest('sampleEndpoint1', api_name='sample')
        self.conn.request_get.assert_called_once_with('apis/sample/endpoints',
                                                headers={'Content-Type': 'application/json',
                                                        'Accept': 'application/json',
                                                        'User-Agent': 'SD-Web'}, args=None)

    @patch('commons.rest_client.rest_client_engine.GENERAL_PARAMETERS', GENERAL_PARAMETERS)
    @patch('commons.rest_client.rest_client_engine.REQUESTS', REQUESTS)
    def test_rest_client_sample1_without_path_variable_should_raise_exception(self):
        self.assertRaises(NotFoundException, self.rest_client_engine.executeRequest, 'sampleEndpoint1')

    @patch('commons.rest_client.rest_client_engine.GENERAL_PARAMETERS', GENERAL_PARAMETERS)
    @patch('commons.rest_client.rest_client_engine.REQUESTS', REQUESTS)
    def test_rest_client_sample1_should_perform_post_request(self):
        self.rest_client_engine.executeRequest('sampleEndpoint2')
        self.conn.request_post.assert_called_once_with('apis', body=None,
                                                       headers={'Custom-Header': 'My Custom Header',
                                                                'Content-Type': 'application/json',
                                                                'Accept': 'application/json',
                                                                'User-Agent': 'SD-Web'})

    @patch('commons.rest_client.rest_client_engine.GENERAL_PARAMETERS', GENERAL_PARAMETERS)
    @patch('commons.rest_client.rest_client_engine.REQUESTS', REQUESTS)
    def test_rest_client_sample5_unknown_method_should_raise_exception(self):
        self.assertRaises(NotFoundException, self.rest_client_engine.executeRequest, 'sampleEndpoint5')

    @patch('commons.rest_client.rest_client_engine.GENERAL_PARAMETERS', GENERAL_PARAMETERS)
    @patch('commons.rest_client.rest_client_engine.REQUESTS', REQUESTS)
    def test_rest_client_unknown_request_should_raise_exception(self):
        self.assertRaises(NotFoundException, self.rest_client_engine.executeRequest, 'unknownRequest')

    @patch('commons.rest_client.rest_client_engine.GENERAL_PARAMETERS', GENERAL_PARAMETERS)
    @patch('commons.rest_client.rest_client_engine.REQUESTS', REQUESTS)
    def test_rest_client_sample3_should_perform_put_request(self):
        self.rest_client_engine.executeRequest('sampleEndpoint3', api_name='api', id='123')
        self.conn.request_put.assert_called_once_with('apis/api/123', body=None,
                                                      headers={'Custom-Header': 'My Custom Header',
                                                               'Content-Type': 'application/json',
                                                               'Accept': 'application/json',
                                                               'User-Agent': 'SD-Web'})

    @patch('commons.rest_client.rest_client_engine.GENERAL_PARAMETERS', GENERAL_PARAMETERS)
    @patch('commons.rest_client.rest_client_engine.REQUESTS', REQUESTS)
    def test_rest_client_sample4_should_perform_delete_request(self):
        self.rest_client_engine.executeRequest('sampleEndpoint4')
        self.conn.request_delete.assert_called_once_with('apis', headers={'Content-Type': 'application/json',
                                                                          'Accept': 'application/json',
                                                                          'User-Agent': 'SD-Web'})

    @patch('commons.rest_client.rest_client_engine.GENERAL_PARAMETERS', GENERAL_PARAMETERS)
    @patch('commons.rest_client.rest_client_engine.REQUESTS', REQUESTS)
    def test_rest_client_sample4_whit_custom_headers_should_perform_delete_request(self):
        self.rest_client_engine.executeRequest('sampleEndpoint4', headers={'MyHeader': 'MyValue'})
        self.conn.request_delete.assert_called_once_with('apis', headers={'MyHeader': 'MyValue',
                                                                          'Content-Type': 'application/json',
                                                                          'Accept': 'application/json',
                                                                          'User-Agent': 'SD-Web'})

    def tearDown(self):
        self.conn.reset_mock()
