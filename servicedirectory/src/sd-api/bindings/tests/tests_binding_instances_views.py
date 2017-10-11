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

class_name = 'test'
url_class_collection = '/sd/v1/classes'
url_get_binding = '/sd/v1/bind_instances?class_name={0}&'
url_instance_collection = '/sd/v1/classes/{0}/instances'
url_bindings_collection = '/sd/v1/bindings/'


class BindingInstancesViewTests(TestCase):

    def test_bind_instances_without_rules_should_raise_404(self):
        # Create an class
        class_ = {'class_name': 'test_bind', 'description': 'Descripcion test', 'default_version': "1.0"}
        instance = {'uri': 'url_test', 'version': '1.0'}
        instance2 = {'uri': 'url_test_2', 'version': '2.0'}
        resp = self.post(url_class_collection, json.dumps(class_))
        self.assertEquals(resp.status_code, 201)
        url_instance_bind = url_get_binding.format('test_bind')

        resp = self.post(url_instance_collection.format('test_bind'), json.dumps(instance))
        self.assertEquals(resp.status_code, 201)
        resp = self.post(url_instance_collection.format('test_bind'), json.dumps(instance2))
        self.assertEquals(resp.status_code, 201)

        # Discover all instances are returned ordered by version
        resp = self.get(url_instance_bind)
        self.assertEquals(resp.status_code, 404)
        response_content = json.loads(resp.content)
        self.assertEquals("SVC2002", response_content['exceptionId'], 'Not correct unica message')
        # Discover instances of given version
        resp = self.get(url_instance_bind + 'version=2.0')
        self.assertEquals(resp.status_code, 404)
        response_content = json.loads(resp.content)
        self.assertEquals("SVC2002", response_content['exceptionId'], 'Not correct unica message')

    def test_bind_instances_with_rules_should_return_matched_rules(self):
        # Create an class
        class_ = {'class_name': 'test_bind_with_rules', 'description': 'Descripcion test',
                  'default_version': "1.0"}
        instance = {'uri': 'url_test', 'version': '1.0', 'attributes': {'protocol': 'https'}}
        instance2 = {'uri': 'url_test_2', 'version': '2.0'}
        resp = self.post(url_class_collection, json.dumps(class_))
        self.assertEquals(resp.status_code, 201)
        url_instance_bind = url_get_binding.format(class_['class_name'])
        resp = self.post(url_instance_collection.format(class_['class_name']), json.dumps(instance))
        self.assertEquals(resp.status_code, 201)
        instance['id'] = json.loads(resp.content)['id']
        resp = self.post(url_instance_collection.format(class_['class_name']), json.dumps(instance2))
        self.assertEquals(resp.status_code, 201)
        instance2['id'] = json.loads(resp.content)['id']

        # add a couple of rules ...
        rules_test = {
            'class_name': class_['class_name'],
            'origin': 'test-rules',
            'binding_rules': [
                {
                 'bindings':[instance['id']],
                 'group_rules': [{'operation':'eq', 'input_context_param':'ob', 'value': ['es']}]
                },
                {
                 'bindings':[instance2['id']],
                 'group_rules': [{'operation':'in', 'input_context_param':'ob', 'value': ['uk']}]
                }, {
                 'bindings':[instance2['id']],
                 'group_rules': [{'operation':'regex', 'input_context_param':'ob', 'value': ['^gbr$']}]
                },
                {
                 'bindings':[instance2['id']],
                 'group_rules': [{'operation':'range', 'input_context_param':'uuid', 'value': [100, 200]}]
                }
            ]
        }
        resp = self.post(url_bindings_collection, json.dumps(rules_test))
        self.assertEquals(resp.status_code, 201)

        # Discover instances for ob es
        resp = self.get(url_instance_bind + 'ob=es&origin=test-rules')
        response_content = json.loads(resp.content)
        self.assertEquals(resp.status_code, 200)
        self.assertEquals("url_test", response_content['uri'], "instances bind by rules was not correct")
        # Discover instances for ob uk
        resp = self.get(url_instance_bind + 'ob=uk&origin=test-rules&filters=uri')
        response_content = json.loads(resp.content)
        self.assertEquals(resp.status_code, 200)
        self.assertEquals("url_test_2", response_content['uri'], "instances bind by rules was not correct")
        self.assertTrue('version' not in response_content)
        # Discover instances without default rules
        resp = self.get(url_instance_bind + 'ob=uk')
        response_content = json.loads(resp.content)
        self.assertEquals(resp.status_code, 404)
        self.assertEquals('SVC2002', response_content['exceptionId'], 'Invalid search by default')
        # Discover instances without rules
        resp = self.get(url_instance_bind + 'ob=uk&origin=no-client')
        response_content = json.loads(resp.content)
        self.assertEquals(resp.status_code, 404)
        self.assertEquals('SVC2002', response_content['exceptionId'], 'Invalid search by no origin')
        # Discover instances without matching rules
        resp = self.get(url_instance_bind + 'ob=br&origin=test-rules')
        response_content = json.loads(resp.content)
        self.assertEquals(resp.status_code, 404)
        self.assertEquals('SVC1006', response_content['exceptionId'], 'Invalid search by no origin')

    def test_bind_instances_with_invalid_query_parameters_should_return_400(self):
        # Create an class
        class_ = {'class_name': 'test_bind2_with_rules', 'description': 'Descripcion test',
                  'default_version': "1.0"}
        instance = {'uri': 'url_test', 'version': '1.0', 'attributes': {'protocol': 'https'}}
        instance2 = {'uri': 'url_test_2', 'version': '2.0'}
        resp = self.post(url_class_collection, json.dumps(class_))
        self.assertEquals(resp.status_code, 201)
        url_instance_bind = url_get_binding.format(class_['class_name'])
        resp = self.post(url_instance_collection.format(class_['class_name']), json.dumps(instance))
        self.assertEquals(resp.status_code, 201)
        instance['id'] = json.loads(resp.content)['id']
        resp = self.post(url_instance_collection.format(class_['class_name']), json.dumps(instance2))
        self.assertEquals(resp.status_code, 201)
        instance2['id'] = json.loads(resp.content)['id']

        # add a couple of rules ...
        rules_test = {
            'class_name': class_['class_name'],
            'origin': 'test-rules',
            'binding_rules': [
                {
                 'bindings':[instance['id']],
                 'group_rules': [{'operation':'eq', 'input_context_param':'ob', 'value': ['es']}]
                },
                {
                 'bindings':[instance2['id']],
                 'group_rules': [{'operation':'in', 'input_context_param':'ob', 'value': ['uk']}]
                }, {
                 'bindings':[instance2['id']],
                 'group_rules': [{'operation':'regex', 'input_context_param':'ob', 'value': ['^gbr$']}]
                },
                {
                 'bindings':[instance2['id']],
                 'group_rules': [{'operation':'range', 'input_context_param':'uuid', 'value': [100, 200]}]
                }
            ]
        }
        resp = self.post(url_bindings_collection, json.dumps(rules_test))
        self.assertEquals(resp.status_code, 201)

        # Discover instances with empty ob
        resp = self.get(url_instance_bind + 'ob=&origin=test-rules')
        response_content = json.loads(resp.content)
        self.assertEquals(resp.status_code, 400)
        self.assertEquals("SVC0002", response_content['exceptionId'], "instances bind by rules was not correct")
        self.assertEquals("Invalid parameter value: empty-query-parameter", response_content['exceptionText'],
                          "instances bind by rules was not correct")

        resp = self.get(url_instance_bind + 'ob=es&atributes.custom=&origin=test-rules')
        response_content = json.loads(resp.content)
        self.assertEquals(resp.status_code, 400)
        self.assertEquals("SVC1001", response_content['exceptionId'], "instances bind by rules was not correct")
        self.assertEquals("Invalid parameter: atributes.custom", response_content['exceptionText'],
                          "instances bind by rules was not correct")

        # Discover instances with duplicated ob
        resp = self.get(url_instance_bind + 'ob=es&ob=espa&origin=test-rules')
        response_content = json.loads(resp.content)
        self.assertEquals(resp.status_code, 400)
        self.assertEquals("SVC1024", response_content['exceptionId'], "instances bind by rules was not correct")
        self.assertEquals("Repeated query parameter: ob", response_content['exceptionText'],
                          "instances bind by rules was not correct")

    def test_bind_instances_with_unexisting_class_should_return_not_found(self):
        url_instance_bind = url_get_binding.format('test_class_not_existing')
        # Discover premiun default instances
        resp = self.get(url_instance_bind + 'version=1.0')
        self.assertEquals(resp.status_code, 404)

    def test_bind_instances_invalid_keys_no_rules_should_return_404(self):
        # Create an class
        class_ = {'class_name': 'test_bind_behaviour2', 'description': 'Descripcion test',
                  'default_version': "1.0"}
        instance = {'uri': 'url_test', 'version': '1.0'}
        instance2 = {'uri': 'url_test_2', 'version': '2.0'}
        resp = self.post(url_class_collection, json.dumps(class_))
        self.assertEquals(resp.status_code, 201)
        url_instance_bind = url_get_binding.format('test_bind_behaviour2')
        resp = self.post(url_instance_collection.format(class_['class_name']), json.dumps(instance))
        self.assertEquals(resp.status_code, 201)
        resp = self.post(url_instance_collection.format(class_['class_name']), json.dumps(instance2))
        self.assertEquals(resp.status_code, 201)

        # try to discover invalid key
        resp = self.get(url_instance_bind + 'non_valid_key=test&behaviour=param_check_strict')
        self.assertEquals(resp.status_code, 404)
        response_content = json.loads(resp.content)
        self.assertEquals("SVC2002", response_content['exceptionId'], 'Not correct unica message returned')
