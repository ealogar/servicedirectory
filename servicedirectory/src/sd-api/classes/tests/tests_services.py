'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
from unittest import TestCase
from mock import MagicMock, patch
from classes.services import ServiceInstanceService, ServiceClassService
from commons.exceptions import GenericServiceError, NotFoundException,\
    UnsupportedParameterValueException, BadParameterException
from commons.test_utils import DictMatcher
from pymongo.errors import OperationFailure


class InstancesServiceTests(TestCase):
    mock_class_dao = MagicMock(name='mock_class_dao')
    mock_instance_dao = MagicMock(name='mock_instance_dao')
    mock_binding_dao = MagicMock(name='binding_dao')

    @classmethod
    def setUpClass(cls):
        super(InstancesServiceTests, cls).setUpClass()
        # Make that instances of classes and instances dao point the mocks
        cls.service = ServiceInstanceService()

        # monkey patching daos for the execution of this class
        cls.patcher_class_dao = patch.object(cls.service, 'class_dao', cls.mock_class_dao)  # @UndefinedVariable
        cls.patcher_instance_dao = patch.object(cls.service, 'instance_dao',  # @UndefinedVariable
                                                cls.mock_instance_dao)
        cls.patcher_binding_dao = patch.object(cls.service, 'binding_dao',  # @UndefinedVariable
                                               cls.mock_binding_dao)
        cls.patcher_class_dao.start()
        cls.patcher_instance_dao.start()
        cls.patcher_binding_dao.start()

    @classmethod
    def tearDownClass(cls):
        cls.patcher_class_dao.stop()
        cls.patcher_instance_dao.stop()
        cls.patcher_binding_dao.stop()
        # Access Singleton and remove ServiceInstanceService singleton
        super(InstancesServiceTests, cls).tearDownClass()

    def setUp(self):
        super(InstancesServiceTests, self).setUp()
        self.mock_class_dao.reset_mock()
        self.mock_binding_dao.reset_mock()
        self.mock_binding_dao.find_by_class_and_origin.reset_mock()
        self.mock_instance_dao.find.reset_mock()
        self.mock_instance_dao.reset_mock()
        self.mock_instance_dao.update.reset_mock()

    def test_discover_instances_no_rules_should_return_all(self):
        self.mock_instance_dao.find_instances.return_value = [{'uri': 'http://uno'}, {'uri': 'http://dos'}]
        instances = self.service.discover_service_instances('test', {})
        self.mock_class_dao.find.assert_called_once_with('test')
        self.mock_instance_dao.find_instances.assert_called_once_with({'class_name': 'test'})
        self.assertEquals(2, len(instances), "Not all instances returned")

    def test_discover_instances_filter_by_class_name_should_raise_badParam(self):
        self.mock_instance_dao.find_instances.return_value = [{'uri': 'http://uno'}, {'uri': 'http://dos'}]
        self.assertRaises(BadParameterException, self.service.discover_service_instances,
                          'test', {'class_name': 'test'})
        self.assertEquals(0, self.mock_class_dao.find.call_count)
        self.assertEquals(0, self.mock_instance_dao.find_instances.call_count)

    def test_update_instance_should_work(self):
        self.mock_instance_dao.update.return_value = True
        instance = {'_id': '52c577679078b9023b3a2c4b', 'uri': 'http://test2', 'version': '2.0'}
        res = self.service.update(instance)
        self.assertEquals(instance, res)
        expectedUpdate = DictMatcher({'_id': '52c577679078b9023b3a2c4b', 'uri': 'http://test2', 'version': '2.0'}, [])
        self.mock_instance_dao.update.assert_called_once_with(expectedUpdate)

    def test_update_instance_db_faile_should_raise_Genericerror(self):
        self.mock_instance_dao.update.return_value = False
        instance = {'_id': '52c577679078b9023b3a2c4b', 'uri': 'http://test2', 'version': '2.0'}
        self.assertRaises(GenericServiceError, self.service.update, instance)
        expectedUpdate = DictMatcher({'_id': '52c577679078b9023b3a2c4b', 'uri': 'http://test2', 'version': '2.0'}, [])
        self.mock_instance_dao.update.assert_called_once_with(expectedUpdate)

    def test_delete_unexisting_class_should_raise_NotFound(self):
        self.mock_class_dao.find.return_value = None
        self.assertRaises(NotFoundException, self.service.delete, 'class', '52c577679078b9023b3a2c4b')
        self.assertEquals(0, self.mock_instance_dao.find.call_count, "instance dao was called")
        self.assertEquals(0, self.mock_instance_dao.delete.call_count, "instance dao delete was called")

    def test_delete_unexisting_instance_should_raise_NotFound(self):
        self.mock_class_dao.find.return_value = {'class_name': 'class', 'version': '1.0'}
        self.mock_instance_dao.find.return_value = None
        self.assertRaises(NotFoundException, self.service.delete, 'class', '52c577679078b9023b3a2c4b')
        self.mock_instance_dao.find.assert_called_once_with('52c577679078b9023b3a2c4b')
        self.assertEquals(0, self.mock_instance_dao.delete.call_count, "instance dao delete was called")

    def test_delete_non_class_instance_should_raise_UnsupportedParameterValueException(self):
        self.mock_class_dao.find.return_value = {'class_name': 'class', 'version': '1.0'}
        self.mock_instance_dao.find.return_value = {'class_name': 'another-class', 'id': '52c577679078b9023b3a2c4b',
                                                    'url': 'http://test2', 'version': '2.0'}
        self.assertRaises(UnsupportedParameterValueException, self.service.delete, 'class', '52c577679078b9023b3a2c4b')
        self.mock_instance_dao.find.assert_called_once_with('52c577679078b9023b3a2c4b')
        self.assertEquals(0, self.mock_instance_dao.delete.call_count, "instance dao delete was called")

    def test_delete_instance_failing_delete_mongo_should_raise_GenericServiceError(self):
        self.mock_class_dao.find.return_value = {'class_name': 'class', 'version': '1.0'}
        self.mock_instance_dao.find.return_value = {'class_name': 'class', 'id': '52c577679078b9023b3a2c4b',
                                                    'uri': 'http://test2', 'version': '2.0'}
        self.mock_instance_dao.delete.return_value = False
        self.assertRaises(GenericServiceError, self.service.delete, 'class', '52c577679078b9023b3a2c4b')
        self.mock_instance_dao.find.assert_called_once_with('52c577679078b9023b3a2c4b')
        self.mock_instance_dao.delete.assert_called_once_with('52c577679078b9023b3a2c4b')

    def test_get_instance_non_existing_class_should_raise_notFound(self):
        self.mock_class_dao.find.return_value = None
        self.mock_instance_dao.find.return_value = {'class_name': 'another-class', 'id': '52c577679078b9023b3a2c4b',
                                                    'uri': 'http://test2', 'version': '2.0'}
        self.assertRaises(NotFoundException, self.service.get_service_instance, 'class', '52c577679078b9023b3a2c4b')
        self.mock_class_dao.find.assert_called_once_with('class')
        self.assertEquals(0, self.mock_instance_dao.find.call_count, "instance dao find was called")

    def test_get_instance_non_valid_class_should_raise_UnsupportedParameterValueException(self):
        self.mock_class_dao.find.return_value = {'class_name': 'class', 'version': '1.0'}
        self.mock_instance_dao.find.return_value = {'class_name': 'another-class', 'id': '52c577679078b9023b3a2c4b',
                                                    'url': 'http://test2', 'version': '2.0'}
        self.assertRaises(UnsupportedParameterValueException, self.service.get_service_instance, 'class',
                          '52c577679078b9023b3a2c4b')
        self.mock_class_dao.find.assert_called_once_with('class')
        self.mock_instance_dao.find.assert_called_once_with('52c577679078b9023b3a2c4b')


class ClassesServiceTests(TestCase):
    mock_class_dao = MagicMock(name='mock_class_dao')
    mock_instance_dao = MagicMock(name='mock_instance_dao')

    @classmethod
    def setUpClass(cls):
        super(ClassesServiceTests, cls).setUpClass()
        # Make that instances of classes and instances dao point the mocks
        cls.service = ServiceClassService()

        # monkey patching daos for the execution of this class
        cls.patcher_class_dao = patch.object(cls.service, 'class_dao', cls.mock_class_dao)  # @UndefinedVariable
        cls.patcher_instance_dao = patch.object(cls.service, 'instance_dao',  # @UndefinedVariable
                                                cls.mock_instance_dao)
        cls.patcher_class_dao.start()
        cls.patcher_instance_dao.start()

    @classmethod
    def tearDownClass(cls):
        cls.patcher_class_dao.stop()
        cls.patcher_instance_dao.stop()
        # Access Singleton and remove ServiceInstanceService singleton
        super(ClassesServiceTests, cls).tearDownClass()

    def setUp(self):
        super(ClassesServiceTests, self).setUp()
        self.mock_class_dao.update_rules.reset_mock()
        self.mock_instance_dao.delete_by_class_name.reset_mock()
        self.mock_class_dao.delete.reset_mock()
        self.mock_class_dao.reset_mock()
        self.mock_instance_dao.find_by_class_name_and_id.reset_mock()
        self.mock_instance_dao.find_instances.reset_mock()
        self.mock_instance_dao.reset_mock()

    def test_delete_class_fail_delete_instance_should_raise_generic_exception(self):
        self.mock_class_dao.find.return_value = {'class_name': 'test', 'version': '1.0', 'rules': None}
        self.mock_instance_dao.delete_by_class_name.side_effect = OperationFailure('can not')
        self.assertRaises(GenericServiceError, self.service.delete, 'test')
        self.mock_class_dao.find.assert_called_once_with('test')
        self.mock_instance_dao.delete_by_class_name.assert_called_once_with('test')
        self.assertEquals(0, self.mock_class_dao.delete.call_count, "class dao delete was called")

    def test_delete_class_fail_delete_class_should_raise_generic_exception(self):
        self.mock_class_dao.find.return_value = {'class_name': 'test', 'version': '1.0', 'rules': None}
        self.mock_instance_dao.delete_by_class_name.return_value = True
        self.mock_class_dao.delete.return_value = False
        self.assertRaises(GenericServiceError, self.service.delete, 'test')
        self.mock_class_dao.find.assert_called_once_with('test')
        self.mock_instance_dao.delete_by_class_name.assert_called_once_with('test')
        self.mock_class_dao.delete.assert_called_once_with('test')

    def test_update_class_fail_db_should_raise_generic_exception(self):
        self.mock_class_dao.update.return_value = False
        self.assertRaises(GenericServiceError, self.service.update, {'_id': 'test', 'version': '2.0'})
        self.assertEquals(0, self.mock_class_dao.find.call_count, 'find called and it shouldnt')
        expectedDict = DictMatcher({'_id': 'test', 'version': '2.0'})
        self.mock_class_dao.update.assert_called_once_with(expectedDict)
