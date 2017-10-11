'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''

from httpretty import activate, register_uri, GET, POST, PUT, DELETE, last_request  # @UnresolvedImport
import json
import unittest
from com.tdigital.sd.admin.client import Client
from com.tdigital.sd.admin.exceptions import ServerException, SdAdminLibraryException
from requests.exceptions import Timeout, SSLError, TooManyRedirects
from mock import patch


class TestClient(unittest.TestCase):

    # Dictionary with a basic response
    RESPONSE_BASIC = {
            'class_name': 'sms',
            'default_version': '1.0',
            'description': 'Servicio global de sms'
        }

    # Dictionary with query parameters
    QUERY_PARAMETERS = {
            'environment': 'production',
            'version': 'v1'
        }

    RESPONSE_NOT_FOUND = {
        'exceptionId': 'SVC',
        'exceptionText': 'Resourc xxx not found'
    }

    def setUp(self):
        self.base_url = 'http://sd_fake.com/sd/v1/'
        self.client = Client(url=self.base_url, username='admin', password='admin', debug=True)

    def test_init(self):
        client = Client(url='http://sd_fake.com/sd/v1/')
        self.assertEqual('http://sd_fake.com/sd/v1/', client.url)
        # Check that final slash is added automatically
        client = Client(url='http://sd_fake.com/sd/v1')
        self.assertEqual('http://sd_fake.com/sd/v1/', client.url)

    def test_get_url(self):
        self.assertEqual('http://sd_fake.com:80/sd/v1/', Client.get_url('http', 'sd_fake.com', 80, 'v1'))

    def test_prepare_url(self):
        self.assertEqual('http://sd_fake.com/sd/v1/', self.client._prepare_url(''))
        self.assertEqual('http://sd_fake.com/sd/v1/classes/sms', self.client._prepare_url('classes/sms'))
        self.assertEqual('http://sd_fake.com/sd/info', self.client._prepare_url('../info'))

    @activate
    def test_invalid_response(self):
        register_uri(
            GET,
            self.base_url + 'classes/sms',
            body='invalid json',
            content_type='text/plain')
        self.assertRaises(SdAdminLibraryException, self.client.get, 'classes/sms')

    @activate
    def test_timeout(self):
        register_uri(
            GET,
            self.base_url + 'classes/sms',
            body=json.dumps(TestClient.RESPONSE_BASIC),
            content_type='text/plain')

        with patch('com.tdigital.sd.admin.client.request') as req_mock:
            req_mock.side_effect = Timeout('...')
            # Send the request
            self.assertRaises(SdAdminLibraryException, self.client.get, 'classes/sms')

    @activate
    def test_ssl(self):
        register_uri(
            GET,
            self.base_url + 'classes/sms',
            body=json.dumps(TestClient.RESPONSE_BASIC),
            content_type='text/plain')

        with patch('com.tdigital.sd.admin.client.request') as req_mock:
            req_mock.side_effect = SSLError('...')
            # Send the request
            self.assertRaises(SdAdminLibraryException, self.client.get, 'classes/sms')

    @activate
    def test_redirects_exception_is_raised(self):
        register_uri(
            GET,
            self.base_url + 'classes/sms',
            body=json.dumps(TestClient.RESPONSE_BASIC),
            content_type='text/plain')

        with patch('com.tdigital.sd.admin.client.request') as req_mock:
            req_mock.side_effect = TooManyRedirects('...')
            # Send the request
            self.assertRaises(TooManyRedirects, self.client.get, 'classes/sms')

    def test_connection_error(self):
        # Send the request to inexistent server (not using httpretty)
        self.assertRaises(SdAdminLibraryException, self.client.get, 'classes/sms')

    @activate
    def test_debug(self):
        register_uri(
            PUT,
            self.base_url + 'classes/sms',
            status=200,
            body=json.dumps(TestClient.RESPONSE_BASIC),
            content_type='application/json')
        client = Client(url=self.base_url, username='admin', password='admin', debug=True)
        response = client.put('classes/sms', body=TestClient.RESPONSE_BASIC)
        self.assertEqual(response, TestClient.RESPONSE_BASIC)

    @activate
    def test_get_not_found(self):
        register_uri(
            GET,
            self.base_url + 'classes/sms',
            status=404,
            body=json.dumps(TestClient.RESPONSE_NOT_FOUND))
        self.assertRaises(ServerException, self.client.get, 'classes/sms')

    @activate
    def test_get_no_path_no_params(self):
        register_uri(
            GET,
            self.base_url,
            body=json.dumps(TestClient.RESPONSE_BASIC),
            content_type='application/json')
        response = self.client.get('')
        self.assertEqual(response, TestClient.RESPONSE_BASIC)

    @activate
    def test_get_no_path_with_params(self):
        register_uri(
            GET,
            self.base_url,
            body=json.dumps(TestClient.RESPONSE_BASIC),
            content_type='application/json')
        response = self.client.get('', TestClient.QUERY_PARAMETERS)
        self.assertEqual(response, TestClient.RESPONSE_BASIC)
        for key, value in TestClient.QUERY_PARAMETERS.iteritems():
            self.assertEqual(value, last_request().querystring[key][0])

    @activate
    def test_get_with_path_no_params(self):
        register_uri(
            GET,
            self.base_url + 'classes/sms',
            body=json.dumps(TestClient.RESPONSE_BASIC),
            content_type='application/json')
        response = self.client.get('classes/sms')
        self.assertEqual(response, TestClient.RESPONSE_BASIC)

    @activate
    def test_get_with_path_with_params(self):
        register_uri(
            GET,
            self.base_url + 'classes/sms',
            body=json.dumps(TestClient.RESPONSE_BASIC),
            content_type='application/json')
        response = self.client.get('classes/sms', TestClient.QUERY_PARAMETERS)
        self.assertEqual(response, TestClient.RESPONSE_BASIC)
        for key, value in TestClient.QUERY_PARAMETERS.iteritems():
            self.assertEqual(value, last_request().querystring[key][0])

    @activate
    def test_post_with_response_body(self):
        register_uri(
            POST,
            self.base_url + 'classes/sms',
            status=201,
            body=json.dumps(TestClient.RESPONSE_BASIC),
            content_type='application/json')

        # Without body in request
        response = self.client.post('classes/sms')
        self.assertEqual(response, TestClient.RESPONSE_BASIC)

        # With body in request (as a dictionary)
        response = self.client.post('classes/sms', body=TestClient.RESPONSE_BASIC)
        self.assertEqual(response, TestClient.RESPONSE_BASIC)

        # With body in request (as a string)
        response = self.client.post('classes/sms', body=json.dumps(TestClient.RESPONSE_BASIC))
        self.assertEqual(response, TestClient.RESPONSE_BASIC)

    @activate
    def test_post_without_response_body(self):
        register_uri(
            POST,
            self.base_url + 'classes/sms',
            body='',
            status=201)

        # Without body in request
        self.assertRaises(SdAdminLibraryException, self.client.post, 'classes/sms')

        # With body in request
        self.assertRaises(SdAdminLibraryException, self.client.post, 'classes/sms', body=TestClient.RESPONSE_BASIC)

    @activate
    def test_put_with_response_body(self):
        register_uri(
            PUT,
            self.base_url + 'classes/sms',
            status=200,
            body=json.dumps(TestClient.RESPONSE_BASIC),
            content_type='application/json')

        # Without body in request
        response = self.client.put('classes/sms')
        self.assertEqual(response, TestClient.RESPONSE_BASIC)

        # With body in request
        response = self.client.put('classes/sms', body=TestClient.RESPONSE_BASIC)
        self.assertEqual(response, TestClient.RESPONSE_BASIC)

    @activate
    def test_put_without_response_body(self):
        register_uri(
            PUT,
            self.base_url + 'classes/sms',
            body='',
            status=200)

        # Without body in request
        self.assertRaises(SdAdminLibraryException, self.client.put, 'classes/sms')

        # With body in request
        self.assertRaises(SdAdminLibraryException, self.client.put, 'classes/sms', body=TestClient.RESPONSE_BASIC)

    @activate
    def test_delete(self):
        register_uri(
            DELETE,
            self.base_url + 'classes/sms',
            body='',
            status=204)

        response = self.client.delete('classes/sms')
        self.assertIsNone(response)

if __name__ == "__main__":
    unittest.main()
