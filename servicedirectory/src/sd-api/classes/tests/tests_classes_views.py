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

url_info_view = '/sd/info'
url_class_collection = '/sd/v1/classes'
url_class_item = '/sd/v1/classes/{0}'
url_instance_collection = '/sd/v1/classes/{0}/instances/'


class ClassesViewTests(TestCase):
    def setUp(self):
        self.class_ = {'class_name': 'test', 'description': 'Descripcion test', 'default_version': "1.0"}
        self.class_new = {'class_name': 'test2', 'description': 'Descripcion test', 'default_version': "1.0"}
        self.class3 = "{'class_name': 'test2', 'descri"
        self.class4 = {'description': 'Descripcion test', 'default_version': '1.0'}

        self.class5 = {'class_name': 'testdelete1', 'description': 'Descripcion test', 'default_version': '1.0'}
        self.class6 = {'class_name': 'testdelete2', 'description': 'Descripcion test', 'default_version': '1.2.5'}
        self.endpt1 = {'uri': 'http://www.tid1.com', 'ob': 'DE', 'version': '1.2.5'}
        self.endpt2 = {'uri': 'http://www.tid2.com', 'ob': 'ES', 'version': '1.2.5'}
        # Ensure that class is created, no matter if fails with 409
        self.post(url_class_collection, json.dumps(self.class_))

    def test_info_view_should_return_200(self):
        resp = self.get(url_info_view)
        response_content = json.loads(resp.content)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('default_version' in response_content)

    def test_add_new_class_should_return_201(self):
        resp = self.post(url_class_collection, json.dumps(self.class_new))
        response_content = json.loads(resp.content)
        self.assertEqual(resp.status_code, 201)
        self.assertEquals('test2', response_content['class_name'])

    def test_add_new_class_invalid_method_should_return_405(self):
        class_new = {'class_name': 'test2_invalid_method', 'description': 'Descripcion test', 'default_version': "1.0"}
        resp = self.put(url_class_collection, json.dumps(class_new))
        response_content = json.loads(resp.content)
        self.assertEqual(resp.status_code, 405)
        self.assertEquals('Requested Operation does not exist: PUT-ServiceClassCollectionView',
                          response_content['exceptionText'])

    def test_add_new_class_invalid_credentials_should_return_401(self):
        NO_USER_AUTH = 'Basic ' + base64.b64encode('%s:%s' % ('admin', 'test_non_user'))
        resp = self.post(url_class_collection, json.dumps(self.class_new), HTTP_AUTHORIZATION=NO_USER_AUTH)
        self.assertEqual(resp.status_code, 401)

    def test_add_new_class_no_credentials_should_return_403(self):
        resp = self.post(url_class_collection, json.dumps(self.class_new), HTTP_AUTHORIZATION=None)
        self.assertEqual(resp.status_code, 403)

    def test_add_existing_class_should_fail_with_status_400(self):
        resp = self.post(url_class_collection, json.dumps(self.class_))
        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content)
        self.assertEquals(content['exceptionId'], 'SVC1021')
        self.assertEquals(content['exceptionText'],
                          'Invalid parameter value: test. Supported values are: non-existing-class')

    def test_add_non_alphanumeric_class_should_fail_with_status_400(self):
        # Ensure self.class is created
        class_bad = {'class_name': 'A espace', 'description': 'Desc test', 'default_version': '1.2.3'}
        resp = self.post(url_class_collection, json.dumps(class_bad))
        content = json.loads(resp.content)
        self.assertEqual(resp.status_code, 400)
        self.assertEquals(content['exceptionId'], 'SVC0002')
        self.assertEquals(content['exceptionText'], 'Invalid parameter value: A espace')
        class_bad = {'class_name': '$dolar', 'description': 'Desc test', 'default_version': '1.2.3'}
        resp = self.post(url_class_collection, json.dumps(class_bad))
        content = json.loads(resp.content)
        self.assertEqual(resp.status_code, 400)
        self.assertEquals(content['exceptionId'], 'SVC0002')
        self.assertEquals(content['exceptionText'], 'Invalid parameter value: $dolar')

    def test_add_class_with_malformed_json_should_fail_with_status_400(self):
        resp = self.post(url_class_collection, self.class3)
        self.assertEqual(resp.status_code, 400)
        self.assertEquals(resp.data['exceptionId'], 'SVC1023')

    def test_add_class_without_default_version_should_fail_with_status_400(self):
        resp = self.post(url_class_collection, json.dumps({'class_name': 'test_df'}))
        self.assertEqual(resp.status_code, 400)
        self.assertEquals(resp.data['exceptionId'], 'SVC1000')

    def test_add_class_without_classname_should_fail_with_status_400(self):
        resp = self.post(url_class_collection, json.dumps(self.class4))
        self.assertEqual(resp.status_code, 400)
        self.assertEquals(resp.data['exceptionId'], 'SVC1000')
        self.assertEquals(resp.data['exceptionText'], 'Missing mandatory parameter: class_name')

    def test_listing_classs_with_slash_optional_should_work(self):
        """
        Check that we can get classs collection both appending / in url and without it
        """
        resp = self.get(url_class_collection)
        response_content = json.loads(resp.content)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(response_content) > 1, "No class was returned")
        self.assertTrue("class_name" in response_content[0] > 1, "Not valid classs collection called")
        resp = self.get(url_class_collection + '/')
        response_content = json.loads(resp.content)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(response_content) > 1, "No class was returned")
        self.assertTrue("class_name" in response_content[0] > 1, "Not valid classs collection called")

    def test_list_existing_class_should_return_200(self):
        """
        Check that we can get classs collection both appending / in url and without it
        """
        # Ensure we have one class created...
        resp = self.get(url_class_item.format('test'))
        self.assertEquals(resp.status_code, 200)
        response_content = json.loads(resp.content)
        self.assertEquals('1.0', response_content['default_version'])
        self.assertEquals('Descripcion test', response_content['description'])

    def test_list_non_existing_class_should_return_404(self):
        """
        Check that we can get classs collection both appending / in url and without it
        """
        # Ensure we have one class created...
        resp = self.get(url_class_item.format('test_unexisting'))
        self.assertEquals(resp.status_code, 404)
        response_content = json.loads(resp.content)
        self.assertEquals('SVC1006', response_content['exceptionId'])

    def test_update_existing_class_should_return_200(self):
        """
        Check that we can get classs collection both appending / in url and without it
        """
        # Ensure we have one class created...
        resp = self.post(url_class_item.format('test'), json.dumps({'description': 'description_test_updated'}))
        self.assertEquals(resp.status_code, 200)
        response_content = json.loads(resp.content)
        self.assertEquals('1.0', response_content['default_version'])
        self.assertEquals('description_test_updated', response_content['description'])
        # check that _id is not returned
        self.assertEquals('test', response_content['class_name'])

    def test_update_non_existing_class_should_return_404(self):
        """
        Check that we can get classes collection both appending / in url and without it
        """
        # Ensure we have one class created...
        resp = self.post(url_class_item.format('test_non_existing'), json.dumps({'description': 'description_test'}))
        self.assertEquals(resp.status_code, 404)
        response_content = json.loads(resp.content)
        self.assertEquals('SVC1006', response_content['exceptionId'])

    def test_delete_unknown_capability_should_return_404(self):
        resp = self.delete(url_class_item.format('unknown'))
        self.assertEquals(resp.status_code, 404)

    def test_delete_empty_capability_should_return_204(self):
        resp = self.post(url_class_collection, json.dumps(self.class5))
        response_content = json.loads(resp.content)
        self.assertEqual(resp.status_code, 201)
        self.assertEquals('testdelete1', response_content['class_name'])
        resp = self.delete(url_class_item.format('testdelete1'))
        self.assertEquals(resp.status_code, 204)

    def test_delete_not_empty_capability_should_return_404(self):
        resp = self.post(url_class_collection, json.dumps(self.class6))
        response_content = json.loads(resp.content)
        self.assertEqual(resp.status_code, 201)
        self.assertEquals('testdelete2', response_content['class_name'])

        resp = self.post(url_instance_collection.format('testdelete2'), json.dumps(self.endpt1))
        response_content = json.loads(resp.content)
        self.assertEquals('testdelete2', response_content['class_name'])
        self.assertEqual(resp.status_code, 201)

        resp = self.post(url_instance_collection.format('testdelete2'), json.dumps(self.endpt2))
        response_content = json.loads(resp.content)
        self.assertEquals('testdelete2', response_content['class_name'])
        self.assertEqual(resp.status_code, 201)

        resp = self.get(url_instance_collection.format('testdelete2'))
        response_content = json.loads(resp.content)
        self.assertEqual(resp.status_code, 200)
        self.assertEquals(2, len(response_content))

        resp = self.delete(url_class_item.format('testdelete2'))
        self.assertEquals(resp.status_code, 204)
