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
from com.tdigital.sd.admin.classes import Classes


class TestClasses(unittest.TestCase):

    RESPONSE_CLASS_CREATED = {
        'class_name': 'fake',
        'default_version': 'v1.0',
        'description': 'fake test'
    }

    RESPONSE_CLASS_UPDATED = {
        'class_name': 'fake',
        'default_version': 'v2.0',
        'description': 'fake test'
    }

    RESPONSE_CLASSES_FOUND = [
        {
            'class_name': 'fake',
            'default_version': 'v1.0',
            'description': 'fake test'
        },
        {
            'class_name': 'fake',
            'default_version': 'v2.0',
            'description': None
        },
        {
            'class_name': 'fake2',
            'default_version': 'v1.0',
            'description': 'other fake class'
        }
    ]

    def setUp(self):
        self.base_url = 'http://sd_fake.com/sd/v1/'
        self.client = Client(url=self.base_url, username='admin', password='admin')
        self.classes = Classes(self.client)

    @httpretty.activate
    def test_create_class(self):
        httpretty.register_uri(
            httpretty.POST,
            self.base_url + 'classes',
            body=json.dumps(TestClasses.RESPONSE_CLASS_CREATED),
            status=201,
            content_type='application/json')
        response = self.classes.create('fake', 'v1.0', 'fake test')
        self.assertEqual(response, TestClasses.RESPONSE_CLASS_CREATED)

    @httpretty.activate
    def test_find_class(self):
        httpretty.register_uri(
            httpretty.GET,
            self.base_url + 'classes',
            body=json.dumps(TestClasses.RESPONSE_CLASSES_FOUND),
            content_type='application/json')
        response = self.classes.find()
        self.assertEqual(response, TestClasses.RESPONSE_CLASSES_FOUND)

    @httpretty.activate
    def test_get_class(self):
        httpretty.register_uri(
            httpretty.GET,
            self.base_url + 'classes' + '/fake',
            body=json.dumps(TestClasses.RESPONSE_CLASS_CREATED),
            content_type='application/json')
        response = self.classes.get('fake')
        self.assertEqual(response, TestClasses.RESPONSE_CLASS_CREATED)

    @httpretty.activate
    def test_update_class(self):
        httpretty.register_uri(
            httpretty.GET,
            self.base_url + 'classes' + '/fake',
            body=json.dumps(TestClasses.RESPONSE_CLASS_CREATED),
            content_type='application/json')
        httpretty.register_uri(
            httpretty.POST,
            self.base_url + 'classes' + '/fake',
            body=json.dumps(TestClasses.RESPONSE_CLASS_UPDATED),
            status=200,
            content_type='application/json')
        response = self.classes.update('fake', default_version='v2.0')
        self.assertEqual(response, TestClasses.RESPONSE_CLASS_UPDATED)

    @httpretty.activate
    def test_delete_class(self):
        httpretty.register_uri(
            httpretty.DELETE,
            self.base_url + 'classes' + '/fake',
            body='',
            status=204)
        response = self.classes.delete('fake')
        self.assertIsNone(response)


if __name__ == "__main__":
    unittest.main()
