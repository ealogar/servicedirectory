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
from com.tdigital.sd.admin.info import Info
from com.tdigital.sd.admin.exceptions import SdAdminLibraryException


class TestInfo(unittest.TestCase):

    RESPONSE_INFO = {
        'app_name': 'Service Directory', 
        'default_version': 'v1'
    }

    def setUp(self):
        self.base_url = 'http://sd_fake.com/sd/v1/'
        self.client = Client(url=self.base_url, username='admin', password='admin')
        self.info = Info(self.client)

    @httpretty.activate
    def test_info(self):
        httpretty.register_uri(
            httpretty.GET,
            'http://sd_fake.com/sd/info',
            body=json.dumps(TestInfo.RESPONSE_INFO),
            status=200,
            content_type='application/json')
        response = self.info.info()
        self.assertEqual(response, TestInfo.RESPONSE_INFO)

    @httpretty.activate
    def test_info_invalid_json_resp(self):
        httpretty.register_uri(
            httpretty.GET,
            'http://sd_fake.com/sd/info',
            body='{}',
            status=200,
            content_type='application/json')
        self.assertRaises(SdAdminLibraryException, self.info.info)

    @httpretty.activate
    def test_info_invalid_length_json_resp(self):
        httpretty.register_uri(
            httpretty.GET,
            'http://sd_fake.com/sd/info',
            body='90',
            status=200,
            content_type='application/json')
        self.assertRaises(SdAdminLibraryException, self.info.info)

    @httpretty.activate
    def test_info_invalid_json_error_resp(self):
        httpretty.register_uri(
            httpretty.GET,
            'http://sd_fake.com/sd/info',
            body='{"myid" : 90}',
            status=400,
            content_type='application/json')
        self.assertRaises(SdAdminLibraryException, self.info.info)


if __name__ == "__main__":
    unittest.main()
