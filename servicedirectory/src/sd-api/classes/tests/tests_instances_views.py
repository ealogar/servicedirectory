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
from commons.test_utils import TestCase
import re

class_name = 'test'
url_class_collection = '/sd/v1/classes'
url_instance_collection = '/sd/v1/classes/{0}/instances'
url_instance_test_collection = url_instance_collection.format(class_name)
url_instance_item = '/sd/v1/classes/{0}/instances/{1}'.format(class_name, '{0}')


class InstancesViewTests(TestCase):

    def setUp(self):
        self.class_ = {'class_name': 'test', 'description': 'Descripcion test', 'default_version': "1.0"}
        self.instance_new = {'uri': 'url_test', 'version': '1.0', 'environment': 'test'}
        self.instance_new_def_env = {'uri': 'url_test_production', 'version': '1.0'}
        self.instance = {'uri': 'url_test_2', 'version': '1.0', 'environment': 'test'}
        self.instance3 = "{'uri': 'url_test_3', 'version': '1.0"
        # TODO make this with fixtures
        self.post(url_class_collection, json.dumps(self.class_))
        # Ensure self.instance2 is created
        self.post(url_instance_test_collection, json.dumps(self.instance))
        super(InstancesViewTests, self).setUp()

    def test_add_new_instance_should_return_201(self):
        # Ensure class is created
        resp = self.post(url_instance_test_collection, json.dumps(self.instance_new))
        response_content = json.loads(resp.content)
        self.assertEqual(resp.status_code, 201)
        self.assertEquals('test', response_content['class_name'])
        self.assertEquals('url_test', response_content['uri'])
        # Ensure Location header is well returned
        self.assertTrue('Location' in resp, 'Location header was not returned')
        self.assertTrue(re.match(r'http://testserver/sd/v1/classes/test/instances/[0-9a-fA-F]+',
                                 resp['Location']), 'Location header was not well returned')

    def test_add_new_instance_without_environment_should_return_default_environment(self):
        # Ensure class is created
        resp = self.post(url_instance_test_collection, json.dumps(self.instance_new_def_env))
        response_content = json.loads(resp.content)
        self.assertEqual(resp.status_code, 201)
        self.assertEquals('test', response_content['class_name'])
        self.assertEquals('url_test_production', response_content['uri'])
        self.assertEquals('production', response_content['environment'])

    def test_add_existing_instance_should_fail_with_status_409(self):
        """
        When non existing rate, new one is added
        """
        resp = self.post(url_instance_test_collection, json.dumps(self.instance))
        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content)
        self.assertEquals(content['exceptionId'], 'SVC1021')
        self.assertEquals(content['exceptionText'],
                    'Invalid parameter value: test-url_test_2-1.0. Supported values are: non-duplicated-instance')

    def test_add_instance_in_nonexisting_class_should_fail_with_status_404(self):
        """
        When non existing rate, new one is added
        """
        url_non_existing_class = url_instance_collection.format('non_existing_class')
        instance_non_existing = {'uri': 'url_test_no_class', 'version': '1.0', 'environment': 'test'}
        resp = self.post(url_non_existing_class, json.dumps(instance_non_existing))
        self.assertEqual(resp.status_code, 404)

    def test_add_instance_with_malformed_json_should_fail_with_status_400(self):
        resp = self.post(url_instance_test_collection, self.instance3)
        self.assertEqual(resp.status_code, 400)
        self.assertEquals(resp.data['exceptionId'], 'SVC1023')

    def test_add_instance_without_url_should_fail_with_status_400(self):
        resp = self.post(url_instance_test_collection, json.dumps({'version': '1.0'}))
        self.assertEqual(resp.status_code, 400)
        self.assertEquals(resp.data['exceptionId'], 'SVC1000')
        self.assertTrue('uri' in resp.data['exceptionText'],
                         'Error url explanation not returned')

    def test_modify_non_existing_instance_should_fail_with_status_404(self):
        instance = {'uri': 'url_test', 'version': '1.0'}
        resp = self.put(url_instance_item.format('non_existing'), json.dumps(instance))
        self.assertEqual(resp.status_code, 404)
        response_content = json.loads(resp.content)
        self.assertEquals('SVC1006', response_content['exceptionId'])

    def test_modify_existing_instance_matching_another_should_fail_with_status_409(self):
        # First create new instance
        instance = {'uri': 'url_test_modified', 'version': '1.0'}
        resp = self.post(url_instance_test_collection, json.dumps(instance))
        self.assertEqual(resp.status_code, 201)
        response_content = json.loads(resp.content)
        # now modifying instance
        id_ = response_content.pop('id')
        response_content['uri'] = self.instance['uri']
        response_content['version'] = self.instance['version']
        resp = self.put(url_instance_item.format(id_), json.dumps(response_content))
        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content)
        self.assertEquals(content['exceptionId'], 'SVC1021')
        self.assertEquals(content['exceptionText'],
                'Invalid parameter value: test-url_test_2-1.0. Supported values are: non-duplicated-instance')

    def test_listing_instances_with_slash_optional_should_work(self):
        """
        Check that we can get classes collection both appending / in url and without it
        """
        # Ensure we have one class created...
        resp = self.post(url_instance_test_collection, json.dumps(self.instance))
        self.assertTrue(resp.status_code == 200 or resp.status_code == 400, 'instance can not be created')
        resp = self.get(url_instance_test_collection)
        response_content = json.loads(resp.content)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(response_content) > 1, "No instance was returned")
        self.assertTrue("uri" in response_content[0] > 1, "Not valid instances collection called")
        resp = self.get(url_instance_test_collection + '/')
        response_content = json.loads(resp.content)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(response_content) > 1, "No instance was returned")
        self.assertTrue("uri" in response_content[0] > 1, "Not valid instances collection called")

    def test_list_non_existing_instance_should_return_404(self):
        """
        Check that we can get classes collection both appending / in url and without it
        """
        # Ensure we have one class created...
        resp = self.get(url_instance_item.format('test_unexisting'))
        self.assertEquals(resp.status_code, 404)
        response_content = json.loads(resp.content)
        self.assertEquals('SVC1006', response_content['exceptionId'])

    def test_get_instances_with_query_params(self):
        # Create an class
        class_ = {'class_name': 'test_get', 'description': 'Descripcion test', 'default_version': "1.0"}
        instance = {'uri': 'url_test', 'version': '1.0', 'attributes': {'key1': '90'}}
        instance2 = {'uri': 'url_test_2', 'version': '2.0', 'attributes': {'key1': '80', 'key2': 'anotherthing'}}
        resp = self.post(url_class_collection, json.dumps(class_))
        self.assertEquals(resp.status_code, 201)
        url_instance_get = url_instance_collection.format('test_get')
        resp = self.post(url_instance_get, json.dumps(instance))
        self.assertEquals(resp.status_code, 201)
        resp = self.post(url_instance_get, json.dumps(instance2))
        self.assertEquals(resp.status_code, 201)

        # Discover all instances are returned ordered by version
        resp = self.get(url_instance_get)
        response_content = json.loads(resp.content)
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(2, len(response_content), 'Not all instance returned')
        self.assertEquals("2.0", response_content[0]['version'], "instances ordering is not correct")
        self.assertEquals("1.0", response_content[1]['version'], "instances ordering is not correct")
        self.assertEquals("anotherthing", response_content[0]['attributes']['key2'], "attributes not correct")
        # Discover instances of given version
        resp = self.get(url_instance_get + '?version=2.0')
        response_content = json.loads(resp.content)
        self.assertEquals(resp.status_code, 200)
        response_content = json.loads(resp.content)
        self.assertEquals("url_test_2", response_content[0]['uri'], 'Not correct endpoint returned')
        # Discover instances attributes.key
        resp = self.get(url_instance_get + '?attributes.KEY1=80')
        response_content = json.loads(resp.content)
        self.assertEquals(resp.status_code, 200)
        response_content = json.loads(resp.content)
        self.assertEquals("url_test_2", response_content[0]['uri'], 'Not correct endpoint returned')

    def test_get_instances_with_invalid_query_parameters_should_return_400(self):
        # Create an class
        class_ = {'class_name': 'test_get2_with_rules', 'description': 'Descripcion test',
                  'default_version': "1.0"}
        instance = {'uri': 'url_test', 'version': '1.0', 'attributes': {'protocol': 'https'}}
        instance2 = {'uri': 'url_test_2', 'version': '2.0'}
        resp = self.post(url_class_collection, json.dumps(class_))
        self.assertEquals(resp.status_code, 201)
        url_instance_get = url_instance_collection.format(class_['class_name'])
        resp = self.post(url_instance_get, json.dumps(instance))
        self.assertEquals(resp.status_code, 201)
        instance['id'] = json.loads(resp.content)['id']
        resp = self.post(url_instance_get, json.dumps(instance2))
        self.assertEquals(resp.status_code, 201)
        instance2['id'] = json.loads(resp.content)['id']

        # Discover instances with empty version
        resp = self.get(url_instance_get + '?version=&attributes.protocol=https')
        response_content = json.loads(resp.content)
        self.assertEquals(resp.status_code, 400)
        self.assertEquals("SVC0002", response_content['exceptionId'], "instances get was not correct")
        self.assertEquals("Invalid parameter value: empty-query-parameter", response_content['exceptionText'],
                          "instances get was not correct")

        resp = self.get(url_instance_get + '?version=1,0&custom.custom=custom')
        response_content = json.loads(resp.content)
        self.assertEquals(resp.status_code, 400)
        self.assertEquals("SVC1001", response_content['exceptionId'], "instances get by rules was not correct")
        self.assertEquals("Invalid parameter: custom.custom", response_content['exceptionText'],
                          "instances get by rules was not correct")

        # Discover instances with duplicated version
        resp = self.get(url_instance_get + '?version=1.0&version=1.0')
        response_content = json.loads(resp.content)
        self.assertEquals(resp.status_code, 400)
        self.assertEquals("SVC1024", response_content['exceptionId'], "instances get was not correct")
        self.assertEquals("Repeated query parameter: version", response_content['exceptionText'],
                          "instances get by rules was not correct")
        # Discover instances with class_name
        resp = self.get(url_instance_get + '?class_name=mi_class')
        response_content = json.loads(resp.content)
        self.assertEquals(resp.status_code, 400)
        self.assertEquals("SVC1001", response_content['exceptionId'], "instances get by rules was not correct")
        self.assertEquals("Invalid parameter: class_name", response_content['exceptionText'],
                          "instances get by rules was not correct")
        # Discover instances with invalid key
        resp = self.get(url_instance_get + '?invalid_key=mi_key')
        response_content = json.loads(resp.content)
        self.assertEquals(resp.status_code, 400)
        self.assertEquals("SVC1001", response_content['exceptionId'], "instances get by rules was not correct")
        self.assertEquals("Invalid parameter: invalid_key", response_content['exceptionText'],
                          "instances get by rules was not correct")

    def test_get_instances__with_unexisting_class_should_return_not_found(self):
        url_instance_get = url_instance_collection.format('test_class_not_existing')
        # Discover premiun default instances
        resp = self.get(url_instance_get + '?version=1.0')
        self.assertEquals(resp.status_code, 404)

    def test_get_instances_filtering_values_should_return_only_requested(self):
        # Create an class
        class_ = {'class_name': 'test_get_filters', 'description': 'Descripcion test', 'default_version': "1.0"}
        instance = {'uri': 'url_test', 'version': '1.0'}
        instance2 = {'uri': 'url_test_2', 'version': '2.0'}
        resp = self.post(url_class_collection, json.dumps(class_))
        self.assertEquals(resp.status_code, 201)
        url_instance_get = url_instance_collection.format('test_get_filters')
        resp = self.post(url_instance_get, json.dumps(instance))
        self.assertEquals(resp.status_code, 201)
        resp = self.post(url_instance_get, json.dumps(instance2))
        self.assertEquals(resp.status_code, 201)

        # Discover premiun default instances
        resp = self.get(url_instance_get + '?filters=version')
        response_content = json.loads(resp.content)
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(2, len(response_content), 'Not valid lenght of instances returned')
        self.assertEquals(2, len(response_content[0]), 'Filtering of parameters of search is not working')
        self.assertTrue('uri' in response_content[0], 'Url mandatory parameter should be returned')
        self.assertTrue('version' in response_content[0], 'version requested parameter should be returned')

    def test_delete_existing_instance_should_return_204(self):
        # Create non existing
        instance = {'uri': 'url_test_delete', 'version': '1.0'}
        resp = self.post(url_instance_test_collection, json.dumps(instance))
        self.assertEquals(201, resp.status_code, "instance for deletion was not created")
        response_content = json.loads(resp.content)
        resp = self.delete(url_instance_item.format(response_content['id']), {})
        self.assertEqual(resp.status_code, 204)
