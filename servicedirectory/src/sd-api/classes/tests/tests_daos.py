'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
from commons.test_utils import TestCase
from classes.daos import ServiceClassDao, ServiceInstanceDao
from pymongo.errors import DuplicateKeyError, OperationFailure
from mock import MagicMock, patch


class ClassesDaoTests(TestCase):
    mock_coll = MagicMock(name='mock_coll')

    @classmethod
    def setUpClass(cls):
        super(ClassesDaoTests, cls).setUpClass()
        # Make that instances of classs and instances dao point the mocks
        cls.dao_mock = ServiceClassDao()
        cls.dao = ServiceClassDao()

        # monkey patching daos for the execution of this class
        cls.patcher_coll = patch.object(cls.dao_mock, 'dbcoll', cls.mock_coll)  # @UndefinedVariable
        cls.patcher_coll.start()

    def setUp(self):
        self.mock_coll.reset_mock()
        self.mock_coll.update.reset_mock()
        self.class_ = {'_id': 'test', 'description': 'Descripcion test', 'default_version': "1.0"}
        self.class_new = {'_id': 'test2', 'description': 'Descripcion test', 'default_version': "1.0"}
        self.dao.create(self.class_)
        super(ClassesDaoTests, self).setUp()

    def tearDown(self):
        self.dao.delete(self.class_['_id'])

    def test_add_new_class_should_work(self):
        self.dao.create(self.class_new)
        created_class = self.dao.find(self.class_new['_id'])
        self.assertEquals(created_class, self.class_new)
        # Removing created class
        self.dao.delete(created_class['_id'])

    def test_find_existing_class_should_work(self):
        existing_class = self.dao.find('test')
        self.assertEquals(existing_class, self.class_)

    def test_find_all_classs_should_work(self):
        # _id is an objectId but we convert to str representation
        classs_list = self.dao.find_all()
        self.assertEquals(1, len(list(classs_list)))

    def test_add_exisiting_class_should_raiseException(self):
        self.assertRaises(DuplicateKeyError, self.dao.create, self.class_)

    def test_modify_description_existing_class_should_return_true(self):
        res = self.dao.update({'_id': 'test', 'default_version': '1.0', 'description': 'modified_desc'})
        self.assertTrue(res, 'update failed')

    def test_modify_existing_class_without_changing_anything_should_return_true(self):
        res = self.dao.update({'_id': 'test', 'default_version': '1.0',})
        self.assertTrue(res, 'update failed')

    def test_modify_non_existing_class_should_return_false(self):
        res = self.dao.update({'_id': 'test2', 'default_version': '1.0', 'description': 'modified_desc'})
        self.assertFalse(res, 'Non existing class was modified and it shouldnt')

    def test_modify_class_fail_db_should_raise_operation_failure(self):
        self.mock_coll.update.side_effect = OperationFailure('can not')
        self.assertRaises(OperationFailure, self.dao_mock.update,
                          {'_id': 'test2', 'default_version': '1.0', 'description': 'modified_desc'})

    def test_delete_non_existing_class_should_return_false(self):
        res = self.dao.delete('non_exitings_id')
        self.assertEquals(res, False, 'Delete not existing class didnt return false')


class InstancesDaoTests(TestCase):
    def setUp(self):
        self.class_ = {'_id': 'test', 'description': 'Descripcion test', 'default_version': "1.0"}
        self.instance = {'uri': 'http://test', 'version': '1.0', 'class_name': 'test'}
        self.instance_new = {'uri': 'http://testNew', 'version': '1.0', 'class_name': 'test'}
        self.dao = ServiceInstanceDao()
        self.classes_dao = ServiceClassDao()
        self.classes_dao.create(self.class_)
        self.dao.create(self.instance)
        super(InstancesDaoTests, self).setUp()

    def tearDown(self):
        self.dao.delete(self.instance['_id'])
        self.classes_dao.delete(self.class_['_id'])

    def test_add_new_instance_should_work(self):
        self.dao.create(self.instance_new)
        created_instance = self.dao.find(self.instance_new['_id'])
        self.assertEquals(created_instance, self.instance_new)
        # Removing created instance
        self.dao.delete(created_instance['_id'])

    def test_find_existing_instance_should_work(self):
        # _id is an objectId but we convert to str representation
        existing_instance = self.dao.find(str(self.instance['_id']))
        self.assertEquals(existing_instance, self.instance)

    def test_find_instance_by_class_name_and_id_invalid_id_should_return_none(self):
        # _id is an objectId but we convert to str representation
        res = self.dao.find_by_class_name_and_id('test', 'invalid_id')
        self.assertEquals(None, res)

    def test_find_all_existing_instance_should_work(self):
        # _id is an objectId but we convert to str representation
        instances_list = self.dao.find_all('test')
        self.assertEquals(1, len(list(instances_list)))

    def test_add_existing_instance_should_raiseException(self):
        """
        We check than uri, version and class_name are unique for instances collection
        """
        # We don't use self.instance as _id will be populated by setUp method
        # We want ton ensure unique index is being managed
        self.assertRaises(DuplicateKeyError, self.dao.create,
                          {'uri': 'http://test', 'version': '1.0', 'class_name': 'test'})

    def test_modify_existing_instance_should_return_true(self):
        self.instance['ob'] = 'oba'
        res = self.dao.update(self.instance)
        self.assertEquals(True, res, 'ob param not added')

    def test_modify_invalid_instance_id_should_return_false(self):
        self.instance_new['_id'] = '8989_nonExisting'
        res = self.dao.update(self.instance_new)
        self.assertEquals(False, res, 'Non existing instance was modified and it shouldnt')

    def test_modify_non_existing_instance_should_return_false(self):
        self.instance_new['_id'] = '5555b1d2f26ba3088459ffff'
        res = self.dao.update(self.instance_new)
        self.assertEquals(False, res, 'Non existing instance was modified and it shouldnt')

    def test_modify_existing_instance_matching_another_should_return_DuplicateKeyException(self):
        instance_new = self.dao.create(self.instance_new)
        instance_new['uri'] = self.instance['uri']
        instance_new['version'] = self.instance['version']
        self.assertRaises(DuplicateKeyError, self.dao.update, instance_new)

    def test_delete_invalid_instance_id_should_return_false(self):
        res = self.dao.delete('non_exitings_id')
        self.assertEquals(res, False, 'Delete not existing instance didnt return false')

    def test_delete_unexisting_instance_id_should_return_false(self):
        res = self.dao.delete('5555b1d2f26ba3088459ffff')
        self.assertEquals(res, False, 'Delete not existing instance didnt return false')
