'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''

import httpretty
import json
import unittest
from com.tdigital.sd.admin.client import Client
from com.tdigital.sd.admin.instances import Instances


class TestInstances(unittest.TestCase):

    RESPONSE_INSTANCE_CREATED = {
        'api_name': 'fake',
        'version': 'v1.0',
        'url': 'http://fake',
        'environment': 'production',
        'attributes': {}
    }

    RESPONSE_INSTANCES_FOUND = [
        {
        'api_name': 'fake',
        'version': 'v1.0',
        'url': 'http://fake1',
        'environment': 'production',
        'attributes': {}
        },
        {
        'api_name': 'fake',
        'version': 'v1.0',
        'url': 'http://fake2',
        'environment': 'production',
        'attributes': {}
        },
        {
        'api_name': 'fake',
        'version': 'v1.0',
        'url': 'http://fake3',
        'environment': 'production',
        'attributes': {"protocol": 'https'}
        }
    ]


    def setUp(self):
        self.base_url = 'http://sd_fake.com/sd/v1/'
        self.client = Client(url=self.base_url, username='admin', password='admin')
        self.instances = Instances(self.client)


    @httpretty.activate
    def test_create_instance(self):
        httpretty.register_uri(
            httpretty.POST,
            self.base_url + 'classes/fake/instances',
            body=json.dumps(TestInstances.RESPONSE_INSTANCE_CREATED),
            status=201,
            content_type='application/json')
        response = self.instances.create('fake', 'v1.0', 'production', 'http://fakeapi/fake/v1')
        self.assertEqual(response, TestInstances.RESPONSE_INSTANCE_CREATED)

    @httpretty.activate
    def test_find_instance(self):
        httpretty.register_uri(
            httpretty.GET,
            self.base_url + 'classes/fake/instances',
            body=json.dumps(TestInstances.RESPONSE_INSTANCES_FOUND),
            content_type='application/json')
        response = self.instances.find('fake')
        self.assertEqual(response, TestInstances.RESPONSE_INSTANCES_FOUND)


    @httpretty.activate
    def test_get_instance(self):
        httpretty.register_uri(
            httpretty.GET,
            self.base_url + 'classes/fake/instances' + '/11234-32-234-1',
            body=json.dumps(TestInstances.RESPONSE_INSTANCE_CREATED),
            content_type='application/json')
        response = self.instances.get('fake', '11234-32-234-1')
        self.assertEqual(response, TestInstances.RESPONSE_INSTANCE_CREATED)


    @httpretty.activate
    def test_delete_instance(self):
        httpretty.register_uri(
            httpretty.DELETE,
            self.base_url + 'classes/fake/instances' + '/11234-32-234-1',
            body='',
            status=204)
        response = self.instances.delete('fake', '11234-32-234-1')
        self.assertIsNone(response)


if __name__ == "__main__":
    unittest.main()
