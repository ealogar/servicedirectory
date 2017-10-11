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
from django.test.utils import override_settings

url_user_collection = '/sd/v1/users'
url_user_item = '/sd/v1/users/{0}'
url_class_collection = '/sd/v1/classes'
url_class_item = '/sd/v1/classes/{0}'
url_instance_collection = '/sd/v1/classes/{0}/instances'
url_binding = '/sd/v1/bindings'


class UsersViewTests(TestCase):
    def setUp(self):
        self.user_test = {'classes': ['test', 'test-new-class'], 'origins': ['origin-test'], 'username': 'test',
                          'password': "test"}
        self.user_test_auth = 'Basic ' + base64.b64encode('%s:%s' % ('test', 'test'))
        self.user_admin_test = {'is_admin': True, 'username': 'test-admin', 'password': "test-admin"}
        self.user_admin_test_auth = 'Basic ' + base64.b64encode('%s:%s' % ('test-admin', 'test-admin'))
        self.user_new = {'classes': ['test'], 'username': 'test-new', 'password': "test"}
        # Ensure that user and user_admin_test are created, no matter if fails with 409
        self.post(url_user_collection, json.dumps(self.user_admin_test))
        # ensure class exist
        self.post(url_class_collection, json.dumps({'class_name': 'test', 'default_version': '1.0'}))
        self.post(url_class_collection, json.dumps({'class_name': 'test-new-class', 'default_version': '1.0'}),
                         HTTP_AUTHORIZATION=self.user_admin_test_auth)

        self.post(url_user_collection, json.dumps(self.user_test))

        super(UsersViewTests, self).setUp()

    def test_add_new_user_should_return_201(self):
        resp = self.post(url_user_collection, json.dumps(self.user_new))
        response_content = json.loads(resp.content)
        self.assertEqual(resp.status_code, 201)
        self.assertEquals('test-new', response_content['username'])
        self.assertEquals('****', response_content['password'])

    def test_add_new_user_non_existing_class_should_return_400_and_SVC1021(self):
        user = {'classes': ['non-existing-class-svc'], 'username': 'test-new', 'password': "test"}
        resp = self.post(url_user_collection, json.dumps(user))
        response_content = json.loads(resp.content)
        self.assertEqual(resp.status_code, 400)
        self.assertEquals('SVC1021', response_content['exceptionId'])

    def test_add_new_user_invalid_credentials_should_return_401_andSVC1018(self):
        NO_USER_AUTH = 'Basic ' + base64.b64encode('%s:%s' % ('admin', 'test_non_user'))
        resp = self.post(url_user_collection, json.dumps(self.user_new), HTTP_AUTHORIZATION=NO_USER_AUTH)
        self.assertEqual(resp.status_code, 401)
        content = json.loads(resp.content)
        self.assertEquals("SVC1018", content['exceptionId'], 'Invalid unica code returned')
        self.assertEquals("Invalid Credentials",
                          content['exceptionText'], 'Invalid unica message returned')

    def test_add_new_user_non_existing_credentials_should_return_401(self):
        NO_USER_AUTH = 'Basic ' + base64.b64encode('%s:%s' % ('non-existing-user', 'test_non_user'))
        resp = self.post(url_user_collection, json.dumps(self.user_new), HTTP_AUTHORIZATION=NO_USER_AUTH)
        self.assertEqual(resp.status_code, 401)

    def test_get_himself_user_non_admin_credentials_should_return_200(self):
        resp = self.get(url_user_item.format(self.user_test['username']), HTTP_AUTHORIZATION=self.user_test_auth)
        self.assertEqual(resp.status_code, 200)

    def test_add_new_user_no_credentials_should_return_403_and_SVC1019(self):
        resp = self.post(url_user_collection, json.dumps(self.user_new), HTTP_AUTHORIZATION=None)
        self.assertEqual(resp.status_code, 403)
        content = json.loads(resp.content)
        self.assertEquals("SVC1019", content['exceptionId'], 'Invalid unica code returned')
        self.assertEquals("Application cannot use API/Feature",
                          content['exceptionText'], 'Invalid unica message returned')

    def test_add_new_user_non_admin_credentials_should_return_403_and_SVC1013(self):
        NO_ADMIN_AUTH = 'Basic ' + base64.b64encode('%s:%s' % ('test', 'test'))
        resp = self.post(url_user_collection, json.dumps(self.user_new), HTTP_AUTHORIZATION=NO_ADMIN_AUTH)
        self.assertEqual(resp.status_code, 403)
        content = json.loads(resp.content)
        self.assertEquals("SVC1013", content['exceptionId'], 'Invalid unica code returned')
        self.assertEquals("CreateUser Operation is not allowed: invalid-permissions",
                          content['exceptionText'], 'Invalid unica message returned')

    def test_add_existing_user_should_fail_with_status_400_and_SVC002(self):
        resp = self.post(url_user_collection, json.dumps(self.user_test))
        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content)
        self.assertEquals("SVC1021", content['exceptionId'], 'Bad unica code returned')

    def test_listing_users_with_slash_optional_should_work(self):
        """
        Check that we can get classes collection both appending / in url and without it
        """
        resp = self.get(url_user_collection, HTTP_AUTHORIZATION=self.ADMIN_AUTH)
        response_content = json.loads(resp.content)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(response_content) > 1, "No user was returned")
        self.assertTrue("username" in response_content[0] > 1, "Not valid users collection called")
        resp = self.get(url_user_collection + '/', HTTP_AUTHORIZATION=self.ADMIN_AUTH)
        response_content = json.loads(resp.content)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(response_content) > 1, "No user was returned")
        self.assertTrue("username" in response_content[0] > 1, "Not valid users collection called")

    def test_list_existing_user_should_return_200(self):
        """
        Check that we can get users collection both appending / in url and without it
        """
        # Ensure we have one class created...
        resp = self.get(url_user_item.format('test'), HTTP_AUTHORIZATION=self.ADMIN_AUTH)
        self.assertEquals(resp.status_code, 200)
        response_content = json.loads(resp.content)
        self.assertEquals('test', response_content['username'])
        self.assertEquals('****', response_content['password'])

    @override_settings(DEBUG=False)
    def test_list_existing_user_invalid_url_should_return_404(self):
        """
        Check that get invalid url return 404
        """
        # Ensure we have one class created...
        resp = self.get('/sd/v1/myusers', HTTP_AUTHORIZATION=self.ADMIN_AUTH)
        self.assertEquals(resp.status_code, 404)
        response_content = json.loads(resp.content)
        self.assertEquals('SVC1006', response_content['exceptionId'])

    def test_list_non_existing_user_should_return_404(self):
        """
        Check that we can get users collection both appending / in url and without it
        """
        # Ensure we have one class created...
        resp = self.get(url_user_item.format('test_unexisting'), HTTP_AUTHORIZATION=self.ADMIN_AUTH)
        self.assertEquals(resp.status_code, 404)
        response_content = json.loads(resp.content)
        self.assertEquals('SVC1006', response_content['exceptionId'])

    def test_update_existing_user_should_return_200(self):
        """
        Check that we can get users collection both appending / in url and without it
        """
        # Ensure we have one class created...
        resp = self.post(url_user_item.format('test'), json.dumps({'classes': ['test']}))
        self.assertEquals(resp.status_code, 200)
        response_content = json.loads(resp.content)
        self.assertEquals(['test'], response_content['classes'])

    def test_update_admin_user_itself_should_return_403_and_SVC1013(self):
        """
        Check that we can get classes collection both appending / in url and without it
        """
        # Ensure we have one class created...

        resp = self.post(url_user_item.format('test-admin'), json.dumps({'classes': ['test']}),
                         HTTP_AUTHORIZATION=self.user_admin_test_auth)
        self.assertEquals(resp.status_code, 403)
        response_content = json.loads(resp.content)
        self.assertEquals('SVC1013', response_content['exceptionId'])

    def test_update_non_existing_user_should_return_404(self):
        """
        Check that we can get classes collection both appending / in url and without it
        """
        # Ensure we have one class created...
        resp = self.post(url_user_item.format('test_non_existing'), json.dumps({'classes': ['test']}))
        self.assertEquals(resp.status_code, 404)
        response_content = json.loads(resp.content)
        self.assertEquals('SVC1006', response_content['exceptionId'])

    def test_delete_user_without_admin_credentials_should_return_403(self):
        """
        Check that we can get classes collection both appending / in url and without it
        """
        # Ensure we have one class created...
        delete_user = {'classes': ['test'], 'username': 'test-delete', 'password': "test"}
        resp = self.post(url_user_collection, json.dumps(delete_user),
                         HTTP_AUTHORIZATION=self.user_admin_test_auth)
        self.assertEquals(resp.status_code, 201)
        resp = self.delete(url_user_item.format('test-delete'), HTTP_AUTHORIZATION=self.user_test_auth)
        self.assertEquals(resp.status_code, 403)
        # now delete user with valid credentials
        resp = self.delete(url_user_item.format('test-delete'), HTTP_AUTHORIZATION=self.user_admin_test_auth)
        self.assertEquals(resp.status_code, 204)

    def test_delete_default_admin_user_should_return_403_andSVC1013(self):
        """
        Check that we can get classes collection both appending / in url and without it
        """
        # Ensure we have one class created...

        resp = self.delete(url_user_item.format('admin'), HTTP_AUTHORIZATION=self.user_admin_test_auth)
        self.assertEquals(resp.status_code, 403)
        response_content = json.loads(resp.content)
        self.assertEquals('SVC1013', response_content['exceptionId'])

    def test_update_class_non_admin_user_authorized_should_work(self):
        resp = self.post(url_class_item.format('test'), json.dumps({'description': 'test', 'default_version': '1.0'}),
                         HTTP_AUTHORIZATION=self.user_admin_test_auth)
        self.assertEqual(resp.status_code, 200)
        resp = self.delete(url_class_item.format('test'),
                           HTTP_AUTHORIZATION=self.user_test_auth)
        self.assertEquals(resp.status_code, 204)

    def test_add_new_client_rules_non_admin_but_authorized_user_should_work(self):
        # Create class and instance
        resp = self.post(url_instance_collection.format('test-new-class'), json.dumps({'uri': 'url_test_a',
                                                                    'version': '1.0', 'environment': 'test'}))

        response_content = json.loads(resp.content)
        instance_id = response_content['id']
        binding_test = {
            'class_name': 'test-new-class',
            'origin': 'origin-test',
            'binding_rules': [
                {
                 'bindings':[instance_id],
                 'group_rules': [{'operation':'eq', 'input_context_param':'ob', 'value': ['es']},
                                 {'operation':'eq', 'input_context_param':'premium', 'value': [True]}]
                }
            ]
        }
        resp = self.post(url_binding, json.dumps(binding_test),
                        HTTP_AUTHORIZATION=self.user_test_auth)
        self.assertEqual(resp.status_code, 201)
        binding_test = {
            'class_name': 'test-new-class',
            'origin': 'default',
            'binding_rules': [
                {
                 'bindings':[instance_id],
                 'group_rules': [{'operation':'eq', 'input_context_param':'ob', 'value': ['es']},
                                 {'operation':'eq', 'input_context_param':'premium', 'value': [True]}]
                }
            ]
        }
        resp = self.post(url_binding, json.dumps(binding_test),
                        HTTP_AUTHORIZATION=self.user_test_auth)
        self.assertEqual(resp.status_code, 201)
