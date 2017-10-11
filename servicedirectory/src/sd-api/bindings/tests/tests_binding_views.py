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
import base64
from bson.objectid import ObjectId

url_class_collection = '/sd/v1/classes'
url_binding_collection = '/sd/v1/bindings'
url_binding_item = '/sd/v1/bindings/{0}'
url_instance_collection = '/sd/v1/classes/{0}/instances'
url_instance_test_collection = url_instance_collection.format('test')
url_user_collection = '/sd/v1/users'


class BindingsViewTests(TestCase):
    instance_a = {'uri': 'url_test_a', 'version': '1.0', 'environment': 'test'}
    instance_b = {'uri': 'url_test_b', 'version': '1.0'}

    def setUp(self):
        self.class_ = {'class_name': 'test', 'description': 'Description test', 'default_version': "1.0"}
        # Ensure that class is created, no matter if fails with 409
        self.post(url_class_collection, json.dumps(self.class_))
        # Create a couple of instances for defining rules

        if 'id' not in BindingsViewTests.instance_a:
            resp = self.post(url_instance_test_collection, json.dumps(BindingsViewTests.instance_a))
            response_content = json.loads(resp.content)
            BindingsViewTests.instance_a['id'] = response_content['id']
        if 'id' not in BindingsViewTests.instance_b:
            resp = self.post(url_instance_test_collection, json.dumps(BindingsViewTests.instance_b))
            response_content = json.loads(resp.content)
            BindingsViewTests.instance_b['id'] = response_content['id']
        # Now define a rules for creating operation

        super(BindingsViewTests, self).setUp()

    def test_add_new_origin_rules_should_return_201_and_location(self):
        rules_test = {
            'class_name': 'test',
            'origin': 'test-rules',
            'binding_rules': [
                {
                 'bindings':[BindingsViewTests.instance_a['id']],
                 'group_rules': [{'operation':'eq', 'input_context_param':'ob', 'value': ['es']},
                                 {'operation':'eq', 'input_context_param':'premium', 'value': [True]}]
                },
                {
                 'bindings':[BindingsViewTests.instance_a['id']],
                 'group_rules': [{'operation':'eq', 'input_context_param':'premium', 'value': [True]}]
                }
            ]
        }
        resp = self.post(url_binding_collection, json.dumps(rules_test))
        response_content = json.loads(resp.content)
        self.assertEqual(resp.status_code, 201)
        self.assertEquals(rules_test['origin'], response_content['origin'])
        self.assertTrue('Location' in resp, 'Location header was not returned')
        self.assertEquals('http://testserver/sd/v1/bindings/{0}'.format(response_content['id']),
                          resp['Location'], 'Location url was not correct')
        self.assertTrue('_id' not in response_content)

    def test_add_new_default_rules_should_return_201(self):
        rules_test = {
            'class_name': 'test',
            'origin': 'default',
            'binding_rules': [
                {
                 'bindings':[BindingsViewTests.instance_a['id']],
                 'group_rules': []
                }
            ]
        }
        resp = self.post(url_binding_collection, json.dumps(rules_test))
        self.assertEqual(resp.status_code, 201)
        response_content = json.loads(resp.content)
        self.assertEquals('default', response_content['origin'])
        # Check that is well defined in db
        resp = self.get(url_binding_item.format(response_content['id']))
        response_content = json.loads(resp.content)
        self.assertEquals('default', response_content['origin'])

    def test_add_new_rules_two_bindings_should_return_SVC0002(self):
        rules_test = {
            'class_name': 'test',
            'origin': 'two-bindings',
            'binding_rules': [
                {
                 'bindings':[BindingsViewTests.instance_a['id'], BindingsViewTests.instance_b['id']],
                 'group_rules': []
                }
            ]
        }
        resp = self.post(url_binding_collection, json.dumps(rules_test))
        self.assertEqual(resp.status_code, 400)
        response_content = json.loads(resp.content)
        self.assertEquals('SVC0002', response_content['exceptionId'])

    def test_add_new_origin_rules_no_credentials_should_return_403(self):
        rules_test = {
            'class_name': 'test',
            'origin': 'test-origin-rules',
            'binding_rules': [
                {
                 'bindings':[BindingsViewTests.instance_a['id'], BindingsViewTests.instance_b['id']],
                 'group_rules': []
                }
            ]
        }
        resp = self.post(url_binding_collection, json.dumps(rules_test),
                        HTTP_AUTHORIZATION=None)
        response_content = json.loads(resp.content)
        self.assertEqual(resp.status_code, 403)
        self.assertEquals('SVC1019', response_content['exceptionId'])

    def test_delete_rules_should_return_204(self):
        rules_test = {
            'class_name': 'test',
            'origin': 'delete-rules',
            'binding_rules': [
                {
                 'bindings':[BindingsViewTests.instance_b['id']],
                 'group_rules': []
                }
            ]
        }
        resp = self.post(url_binding_collection, json.dumps(rules_test))
        self.assertEqual(resp.status_code, 201)
        response_content = json.loads(resp.content)
        binding_id = response_content['id']
        resp = self.delete(url_binding_item.format(binding_id))
        self.assertEqual(resp.status_code, 204)

    def test_add_rules_invalid_instance_should_return_400(self):
        rules_test = {
            'class_name': 'test',
            'origin': 'test-invalid',
            'binding_rules': [
                {
                 'bindings':['instance_bad'],
                 'group_rules': []
                }
            ]
        }
        resp = self.post(url_binding_collection, json.dumps(rules_test))
        self.assertEqual(resp.status_code, 400)

    def test_add_rules_invalid_operation_should_return_SVC0003(self):
        rules_test = {
            'class_name': 'test',
            'origin': 'test-invalid',
            'binding_rules': [
                {
                 'bindings':[BindingsViewTests.instance_a['id']],
                 'extra-param': True,
                 'group_rules': [{'operation': '\u00f1op', 'input_context_param': 'ob', 'value':['1']}]
                }
            ]
        }
        resp = self.post(url_binding_collection, json.dumps(rules_test))
        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content)
        self.assertEquals('SVC0003', content['exceptionId'])

    def test_add_rules_invalid_schema_should_return_SVC0002(self):
        rules_test = {
            'class_name': 'test',
            'origin': 'test-invalid',
            'binding_rules': [
                {
                 'bindings':[BindingsViewTests.instance_a['id']],
                 'extra-param': True,
                 'group_rules': [{'operation': 'eq', 'input_context_param': 'ob', 'value':[['kye', '1']]}]
                }
            ]
        }
        resp = self.post(url_binding_collection, json.dumps(rules_test))
        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content)
        self.assertEquals('SVC0002', content['exceptionId'])

    def test_add_rules_extra_params_should_return_SVC1000(self):
        rules_test = {
            'class_name': 'test',
            'origin': 'test-invalid',
            'binding_rules': [
                {
                 'bindings':[BindingsViewTests.instance_a['id']],
                 'extra-param': True,
                 'group_rules': [{'input_context_param': 'ob', 'value':[['kye', '1']]}]
                }
            ]
        }
        resp = self.post(url_binding_collection, json.dumps(rules_test))
        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content)
        self.assertEquals('SVC1000', content['exceptionId'])

    def test_add_new_default_rules_bad_default_should_return_400(self):
        rules_test = {
            'class_name': 'test',
            'origin': 'DEFAULT',
            'binding_rules': [
                {
                 'bindings':[BindingsViewTests.instance_a['id']],
                 'group_rules': []
                }
            ]
        }
        resp = self.post(url_binding_collection, json.dumps(rules_test))
        self.assertEqual(resp.status_code, 400)

    def create_class_instance(self, class_name):
        class_all = {'class_name': class_name, 'description': 'Descripcion test', 'default_version': "1.0"}
        # Ensure that class is created, no matter if fails with 409
        resp = self.post(url_class_collection, json.dumps(class_all))
        self.assertEquals(resp.status_code, 201)
        instance = {'uri': class_name + '_test', 'version': '1.0', 'environment': 'production'}
        resp = self.post(url_instance_collection.format(class_all['class_name']), json.dumps(instance))
        response_content = json.loads(resp.content)
        return response_content['id']

    def test_get_rules_should_return_existing(self):
        class_ = 'test-all-rules'
        instance_id = self.create_class_instance(class_)

        # get all rules should return empty
        resp = self.get(url_binding_collection, HTTP_AUTHORIZATION=self.ADMIN_AUTH)
        self.assertEquals(resp.status_code, 200)
        response_content = json.loads(resp.content)

        prev_bindings = len(response_content)

        # add one binding rule
        rules_test = {
            'class_name': 'test-all-rules',
            'origin': 'test-rules',
            'binding_rules': [
                {
                 'bindings':[instance_id],
                 'group_rules': [{'operation':'eq', 'input_context_param':'premium', 'value': [True]}]
                }
            ]
        }
        resp = self.post(url_binding_collection, json.dumps(rules_test))
        response_content = json.loads(resp.content)
        self.assertEquals(resp.status_code, 201)

        # get all rules should return one now
        resp = self.get(url_binding_collection, HTTP_AUTHORIZATION=self.ADMIN_AUTH)
        self.assertEquals(resp.status_code, 200)
        response_content = json.loads(resp.content)
        self.assertEquals(prev_bindings + 1, len(response_content))
        # now we apply filtering query_params
        resp = self.get(url_binding_collection + "?class_name=non-existing&origin=non_existing",
                        HTTP_AUTHORIZATION=self.ADMIN_AUTH)
        self.assertEquals(resp.status_code, 200)
        response_content = json.loads(resp.content)
        self.assertEquals(0, len(response_content))

    def test_create_rules_non_authorized_class_user_should_return_403(self):
        # create custom class
        self.create_class_instance("class-test-new-user")
        # create user non admin with custom class permissions
        user = {'classes': ['class-test-new-user'], 'username': 'test-new-rules', 'password': "test"}
        resp = self.post(url_user_collection, json.dumps(user))
        self.assertEqual(resp.status_code, 201)

        # try to create rules of non authorized class
        auth_custom = 'Basic ' + base64.b64encode('%s:%s' % ('test-new-rules', 'test'))
        rules_test = {
            'class_name': 'test',
            'origin': 'new-origin-test-class',
            'binding_rules': [
                {
                 'bindings':[BindingsViewTests.instance_a['id']],
                 'group_rules': []
                }
            ]
        }
        # get all rules should return empty
        resp = self.post(url_binding_collection, json.dumps(rules_test), HTTP_AUTHORIZATION=auth_custom)
        self.assertEquals(resp.status_code, 403)
        response_content = json.loads(resp.content)
        self.assertEquals("SVC1013", response_content['exceptionId'])

    def test_update_existing_rules_should_return_updated(self):
        class_ = 'test-existing-rules'
        instance_id = self.create_class_instance(class_)

        # add one origin rule
        rules_test = {
            'class_name': 'test-existing-rules',
            'origin': 'test-rules',
            'binding_rules': [
                {
                 'bindings':[instance_id],
                 'group_rules': [{'operation':'eq', 'input_context_param':'premium', 'value': [True]}]
                }
            ]
        }
        resp = self.post(url_binding_collection, json.dumps(rules_test))
        self.assertEquals(resp.status_code, 201)
        response_content = json.loads(resp.content)
        binding_id = response_content['id']
        # delete
        rules_test = {
            'class_name': 'test-existing-rules',
            'origin': 'test-rules',
            'binding_rules': [
                {
                 'bindings':[instance_id],
                 'group_rules': []
                }
            ]
        }
        resp = self.put(url_binding_item.format(binding_id), json.dumps(rules_test))
        self.assertEquals(resp.status_code, 200)
        response_content = json.loads(resp.content)
        self.assertEquals([], response_content['binding_rules'][0]['group_rules'], "Rules not updated")
        # Ensure that get return same object
        resp = self.get(url_binding_collection.format(class_, 'test-rules'), HTTP_AUTHORIZATION=self.ADMIN_AUTH)

    def test_update_unexisting_rules_should_raise_not_found(self):
        binding_id = str(ObjectId())
        rules_test = {
            'class_name': 'test-existing-rules',
            'origin': 'test-rules',
            'binding_rules': [
                {
                 'bindings':[str(ObjectId())],
                 'group_rules': []
                }
            ]
        }
        resp = self.put(url_binding_item.format(binding_id), json.dumps(rules_test))
        self.assertEquals(resp.status_code, 404)
