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
from commons.exceptions import GenericServiceError, NotFoundException, UnsupportedParameterValueException,\
    MissingMandatoryParameterException
from bindings.services import BindingService
from pymongo.errors import DuplicateKeyError
from bindings.exceptions import NotBindingDefinedException,\
    NotMatchingRuleException, NotBindingInstanceException,\
    DeletedInstanceException


class BindingServiceTests(TestCase):
    mock_class_dao = MagicMock(name='mock_class_dao')
    mock_binding_dao = MagicMock(name='mock_binding_dao')
    mock_instance_dao = MagicMock(name='mock_instance_dao')

    @classmethod
    def setUpClass(cls):
        super(BindingServiceTests, cls).setUpClass()
        # Make that instances of classes and instances dao point the mocks
        cls.service = BindingService()

        # monkey patching daos for the execution of this class
        cls.patcher_class_dao = patch.object(cls.service, 'class_dao', cls.mock_class_dao)  # @UndefinedVariable
        cls.patcher_binding_dao = patch.object(cls.service, 'binding_dao',  # @UndefinedVariable
                                                cls.mock_binding_dao)
        cls.patcher_instance_dao = patch.object(cls.service, 'instance_dao',  # @UndefinedVariable
                                                cls.mock_instance_dao)
        cls.patcher_class_dao.start()
        cls.patcher_binding_dao.start()
        cls.patcher_instance_dao.start()

    @classmethod
    def tearDownClass(cls):
        cls.patcher_class_dao.stop()
        cls.patcher_binding_dao.stop()
        cls.patcher_instance_dao.stop()
        # Access Singleton and remove ServiceInstanceService singleton
        super(BindingServiceTests, cls).tearDownClass()

    def setUp(self):
        self.mock_class_dao.find.reset_mock()
        self.mock_instance_dao.find_by_class_name_and_id.reset_mock()
        self.mock_binding_dao.update_binding.reset_mock()
        self.mock_binding_dao.update_binding.side_effect = None
        self.mock_binding_dao.delete.reset_mock()
        self.mock_binding_dao.create.reset_mock()
        self.mock_binding_dao.create.side_effect = None
        self.mock_binding_dao.get_binding_by_id.reset_mock()
        self.mock_binding_dao.reset_mock()
        self.mock_binding_dao.find_by_class_and_origin.reset_mock()
        self.mock_instance_dao.find.reset_mock()
        self.mock_instance_dao.reset_mock()

    def test_get_binding_by_id_not_existing_should_raise_notfound(self):
        self.mock_binding_dao.find.return_value = None
        self.assertRaises(NotFoundException, self.service.get_binding_by_id, '52c577679078b9023b3a2c4b')
        self.mock_binding_dao.find.assert_called_once_with('52c577679078b9023b3a2c4b')

    def test_delete_bindings_should_work(self):
        self.mock_binding_dao.delete.return_value = True
        self.service.delete_binding('test')
        self.mock_binding_dao.delete.assert_called_once_with('test')

    def test_delete_bindings_fail_db_should_raise_GenericServiceError(self):
        self.mock_binding_dao.delete.return_value = False
        self.assertRaises(GenericServiceError, self.service.delete_binding, 'test')
        self.mock_binding_dao.delete.assert_called_once_with('test')

    def test_update_binding_fail_db_should_raise_Exception(self):
        self.mock_class_dao.find.return_value = {'class_name': 'test', 'version': '1.0'}
        self.mock_instance_dao.find_by_class_name_and_id.return_value = {'_id': 'endpoint_id',
                                                                         'uri': 'http://test'}
        binding_rules = {
                   'origin': 'cli-test',
                   'class_name': 'test',
                   '_id': 'binding_id_test',
                   'binding_rules':
                   [
                    {
                     "bindings": ['52c577679078b9023b3a2c4b'],
                     "group_rules": [{'operation': 'in', 'input_context_param': 'uuid', 'value': [1, 300]}]
                    }
                   ]
                 }
        self.mock_binding_dao.update_binding.return_value = False

        self.assertRaises(GenericServiceError, self.service.update_binding, binding_rules)
        self.mock_class_dao.find.assert_called_once_with('test')
        self.mock_binding_dao.update_binding.assert_called_once_with(binding_rules)
        self.mock_instance_dao.find_by_class_name_and_id.assert_called_once_with('test', '52c577679078b9023b3a2c4b')

    def test_update_binding_matching_another_should_raise_UnsupportedParameterValue(self):
        self.mock_class_dao.find.return_value = {'class_name': 'test', 'version': '1.0'}
        self.mock_instance_dao.find_by_class_name_and_id.return_value = {'_id': 'endpoint_id',
                                                                         'uri': 'http://test'}
        binding_rules = {
                   'origin': 'cli-test',
                   'class_name': 'test',
                   '_id': 'binding_id_test',
                   'binding_rules':
                   [
                    {
                     "bindings": ['52c577679078b9023b3a2c4b'],
                     "group_rules": [{'operation': 'in', 'input_context_param': 'uuid', 'value': [1, 300]}]
                    }
                   ]
                 }
        self.mock_binding_dao.update_binding.side_effect = DuplicateKeyError('can not')

        self.assertRaises(UnsupportedParameterValueException, self.service.update_binding, binding_rules)
        self.mock_class_dao.find.assert_called_once_with('test')
        self.mock_binding_dao.update_binding.assert_called_once_with(binding_rules)
        self.mock_instance_dao.find_by_class_name_and_id.assert_called_once_with('test', '52c577679078b9023b3a2c4b')

    def test_update_binding_instance_not_of_class_should_raise_BadParameterValueException(self):
        self.mock_class_dao.find.return_value = {'class_name': 'test', 'version': '1.0'}
        binding = {
                   'origin': 'cli-test',
                   'class_name': 'test',
                   '_id': 'binding_id_test',
                   'binding_rules':
                   [
                    {
                     "bindings": ['52c577679078b9023b3a2c4b'],
                     "group_rules": [{'operation': 'in', 'input_context_param': 'uuid', 'value': [1, 300]}]
                    }
                   ]
                 }
        self.mock_binding_dao.update_binding.return_value = False
        self.mock_instance_dao.find_by_class_name_and_id.return_value = None

        with self.assertRaises(UnsupportedParameterValueException) as cm:
            self.service.update_binding(binding)
        self.assertEquals("Invalid parameter value: 52c577679078b9023b3a2c4b. Supported values are: instances of test",
                          cm.exception._details)
        self.mock_class_dao.find.assert_called_once_with('test')
        self.assertEquals(0, self.mock_binding_dao.update_binding.call_count, 'Update_binding_rules was called')
        self.mock_instance_dao.find_by_class_name_and_id.assert_called_once_with('test', '52c577679078b9023b3a2c4b')

    def test_update_binding_class_name_not_existing_should_raise_NotFoundException(self):
        self.mock_class_dao.find.return_value = None
        binding = {
                   'origin': 'cli-test',
                   'class_name': 'test',
                   '_id': 'binding_id_test_non_existing',
                   'binding_rules':
                   [
                    {
                     "bindings": ['52c577679078b9023b3a2c4b'],
                     "group_rules": [{'operation': 'in', 'input_context_param': 'uuid', 'value': [1, 300]}]
                    }
                   ]
                 }

        with self.assertRaises(NotFoundException) as cm:
            self.service.update_binding(binding)
        self.assertEquals("Resource test does not exist", cm.exception._details)
        self.mock_class_dao.find.assert_called_once_with('test')
        self.assertEquals(0, self.mock_binding_dao.update_binding.call_count, 'Update_binding_rules was called')

    def test_create_binding_class_name_not_existing_should_raise_NotFoundException(self):
        self.mock_class_dao.find.return_value = None
        binding = {
                   'origin': 'cli-test',
                   'class_name': 'test',
                   'binding_rules':
                   [
                    {
                     "bindings": ['52c577679078b9023b3a2c4b'],
                     "group_rules": [{'operation': 'in', 'input_context_param': 'uuid', 'value': [1, 300]}]
                    }
                   ]
                 }

        with self.assertRaises(NotFoundException) as cm:
            self.service.create_binding(binding)
        self.assertEquals("Resource test does not exist", cm.exception._details)
        self.mock_class_dao.find.assert_called_once_with('test')
        self.assertEquals(0, self.mock_binding_dao.create.call_count, 'Create was called')

    def test_create_binding_matching_another_should_raise_UnsupportedParameterValue(self):
        self.mock_class_dao.find.return_value = {'class_name': 'test', 'version': '1.0'}
        self.mock_instance_dao.find_by_class_name_and_id.return_value = {'_id': 'endpoint_id',
                                                                         'uri': 'http://test'}
        binding_rules = {
                   'origin': 'cli-test',
                   'class_name': 'test',
                   '_id': 'binding_id_test',
                   'binding_rules':
                   [
                    {
                     "bindings": ['52c577679078b9023b3a2c4b'],
                     "group_rules": [{'operation': 'in', 'input_context_param': 'uuid', 'value': [1, 300]}]
                    }
                   ]
                 }
        self.mock_binding_dao.create.side_effect = DuplicateKeyError('can not')

        self.assertRaises(UnsupportedParameterValueException, self.service.create_binding, binding_rules)
        self.mock_class_dao.find.assert_called_once_with('test')
        self.mock_binding_dao.create.assert_called_once_with(binding_rules)
        self.mock_instance_dao.find_by_class_name_and_id.assert_called_once_with('test', '52c577679078b9023b3a2c4b')

    def test_discover_instances_with_matching_rules_should_return_one(self):
        instance1 = {'id': '51c577679078b9023b3a2c4b', 'uri': 'http://test', 'version': '1.0'}
        instance2 = {'id': '52cc77679078b9023b3a2c4b', 'uri': 'http://test', 'version': '1.0'}
        self.mock_class_dao.find.return_value = {'class_name': 'class', 'version': '1.0'}
        self.mock_binding_dao.find_by_class_and_origin.return_value = {
            'class_name': 'test',
           'origin': 'cli',
           'binding_rules':
           [
            {
             "bindings": [instance1['id']],
             "group_rules": [{'operation': 'eq', 'input_context_param': 'ob', 'value': ['es']},
                             {'operation': 'range', 'input_context_param': 'uuid', 'value': [1.0, 200.0]}]
            },
            {
             "bindings": [instance2['id']],
             "group_rules": [{'operation': 'in', 'input_context_param': 'ob', 'value': ['es']},
                             {'operation': 'range', 'input_context_param': 'uuid', 'value': [1.0, 200.0]},
                             {'operation': 'eq', 'input_context_param': 'premium', 'value': [False]}]
            }
           ]
         }
        self.mock_instance_dao.find.return_value = instance1

        instances = self.service.get_binding_instance(
                                    {'class_name': 'test', 'origin': 'cli', 'ob': 'es', 'uuid': '4.5'})
        self.assertEquals('http://test', instances['uri'], "No instance returned")
        self.mock_instance_dao.find.assert_called_once_with('51c577679078b9023b3a2c4b')

    def test_discover_instances_with_matching_rules_deleted_instance_should_raise_deleted(self):
        instance1 = {'id': '51c577679078b9023b3a2c4b', 'uri': 'http://test', 'version': '1.0'}
        instance2 = {'id': '52cc77679078b9023b3a2c4b', 'uri': 'http://test', 'version': '1.0'}
        self.mock_class_dao.find.return_value = {'class_name': 'class', 'version': '1.0'}
        self.mock_binding_dao.find_by_class_and_origin.return_value = {
            'class_name': 'test',
           'origin': 'cli',
           'binding_rules':
           [
            {
             "bindings": [instance1['id']],
             "group_rules": [{'operation': 'eq', 'input_context_param': 'ob', 'value': ['es']},
                             {'operation': 'range', 'input_context_param': 'uuid', 'value': [1.0, 200.0]}]
            },
            {
             "bindings": [instance2['id']],
             "group_rules": [{'operation': 'in', 'input_context_param': 'ob', 'value': ['es']},
                             {'operation': 'range', 'input_context_param': 'uuid', 'value': [1.0, 200.0]},
                             {'operation': 'eq', 'input_context_param': 'premium', 'value': [False]}]
            }
           ]
         }
        self.mock_instance_dao.find.return_value = None
        self.assertRaises(DeletedInstanceException, self.service.get_binding_instance,
                          {'class_name': 'test', 'origin': 'cli', 'ob': 'es', 'uuid': '4.5'})
        self.mock_instance_dao.find.assert_called_once_with('51c577679078b9023b3a2c4b')

    def test_discover_instances_no_class_name_should_raise_missing(self):
        instance1 = {'id': '51c577679078b9023b3a2c4b', 'uri': 'http://test', 'version': '1.0'}
        instance2 = {'id': '52cc77679078b9023b3a2c4b', 'uri': 'http://test', 'version': '1.0'}
        self.mock_class_dao.find.return_value = {'class_name': 'class', 'version': '1.0'}
        self.mock_binding_dao.find_by_class_and_origin.return_value = {
            'class_name': 'test',
           'origin': 'cli',
           'binding_rules':
           [
            {
             "bindings": [instance1['id']],
             "group_rules": [{'operation': 'eq', 'input_context_param': 'ob', 'value': ['es']},
                             {'operation': 'range', 'input_context_param': 'uuid', 'value': [1.0, 200.0]}]
            },
            {
             "bindings": [instance2['id']],
             "group_rules": [{'operation': 'in', 'input_context_param': 'ob', 'value': ['es']},
                             {'operation': 'range', 'input_context_param': 'uuid', 'value': [1.0, 200.0]},
                             {'operation': 'eq', 'input_context_param': 'premium', 'value': [False]}]
            }
           ]
         }
        self.mock_instance_dao.find.return_value = instance1
        self.assertRaises(MissingMandatoryParameterException, self.service.get_binding_instance,
                          {'origin': 'cli', 'ob': 'es', 'uuid': '4.5'})
        self.assertEquals(0, self.mock_instance_dao.find.call_count)

    def test_discover_instances_with_matching_rules_no_instances_defined_should_rairse_not_found(self):
        self.mock_class_dao.find.return_value = {'class_name': 'class', 'version': '1.0'}
        self.mock_binding_dao.find_by_class_and_origin.return_value = {
            'class_name': 'test',
           'origin': 'cli',
           'binding_rules':
           [
            {
             "bindings": [],
             "group_rules": [{'operation': 'eq', 'input_context_param': 'ob', 'value': ['es']},
                             {'operation': 'range', 'input_context_param': 'uuid', 'value': [1.0, 200.0]}]
            }
           ]
         }

        self.assertRaises(NotBindingInstanceException, self.service.get_binding_instance,
                                    {'class_name': 'test', 'origin': 'cli', 'ob': 'es', 'uuid': '4.5'})
        self.assertEquals(0, self.mock_instance_dao.find.call_count, 'mock_instance_dao should not be called')

    def test_discover_instances_no_client_rules_should_execute_default(self):
        instance1 = {'_id': '51c577679078b9023b3a2c4b', 'uri': 'http://test', 'version': '1.0'}
        self.mock_class_dao.find.return_value = {'class_name': 'test', 'version': '1.0'}
        self.mock_binding_dao.find_by_class_and_origin.return_value = {
            'class_name': 'test',
            'origin': 'default',
            'binding_rules':
                 [
                    {
                      "bindings": [instance1['_id']],
                      "group_rules": [{'operation': 'eq', 'input_context_param': 'ob', 'value': ['es']}]
                     }
                  ]
            }
        self.mock_instance_dao.find.return_value = instance1

        instances = self.service.get_binding_instance({'class_name': 'test', 'ob': 'es'})
        self.assertEquals('http://test', instances['uri'], "No instance returned")
        self.mock_instance_dao.find.assert_called_once_with(instance1['_id'])
        self.mock_binding_dao.find_by_class_and_origin.assert_called_once_with('test',  'default')

    def test_discover_instances_non_existing_client_rule_should_raise_exception(self):
        self.mock_class_dao.find.return_value = {'class_name': 'class', 'version': '1.0'}
        self.mock_binding_dao.find_by_class_and_origin.return_value = None

        self.assertRaises(NotBindingDefinedException, self.service.get_binding_instance,
                          {'class_name': 'test', 'origin': 'non-cli', 'ob': 'es'})
        self.assertEquals(0, self.mock_instance_dao.call_count, "instance dao was called")
        self.mock_binding_dao.find_by_class_and_origin.assert_called_once_with('test', 'non-cli')

    def test_discover_instances_with_rules_bad_range_query_param_should_raise_exception(self):
        instance2 = {'id': '52c577679078b9023b3a2c4b', 'uri': 'http://test2', 'version': '2.0'}
        self.mock_class_dao.find.return_value = {'class_name': 'test', 'version': '1.0'}
        self.mock_binding_dao.find_by_class_and_origin.return_value = {
           'class_name': 'test',
           'origin': 'cli',
           'binding_rules':
           [
            {
             "bindings": [instance2['id']],
             "group_rules": [{'operation': 'range', 'input_context_param': 'uuid', 'value': [1, 200]}]
            }
           ]
            }
        self.assertRaises(UnsupportedParameterValueException, self.service.get_binding_instance,
                          {'class_name': 'test', 'origin': 'cli', 'uuid': 'es'})
        self.assertEquals(0, self.mock_instance_dao.call_count, "instance dao was called")
        self.assertRaises(UnsupportedParameterValueException, self.service.get_binding_instance,
                          {'class_name': 'test', 'origin': 'cli', 'uuid': '5,5'})
        self.assertEquals(0, self.mock_instance_dao.call_count, "instance dao was called")
        self.assertRaises(UnsupportedParameterValueException, self.service.get_binding_instance,
                          {'class_name': 'test', 'origin': 'cli', 'uuid': 'True'})
        self.assertEquals(0, self.mock_instance_dao.call_count, "instance dao was called")

    def test_discover_instances_with_rules_int_query_param_in_range_float_should_raise_exception(self):
        instance2 = {'id': '52c577679078b9023b3a2c4b', 'uri': 'http://test2', 'version': '2.0'}
        self.mock_class_dao.find.return_value = {'class_name': 'test', 'version': '1.0'}
        self.mock_binding_dao.find_by_class_and_origin.return_value = {
              'class_name': 'test',
              'origin': 'cli',
              'binding_rules':
              [
               {
                "bindings": [instance2['id']],
                "group_rules": [{'operation': 'range', 'input_context_param': 'uuid', 'value': [1.0, 200.0]}]
               }
              ]
            }

        self.assertRaises(UnsupportedParameterValueException, self.service.get_binding_instance,
                          {'class_name': 'test', 'origin': 'cli', 'uuid': '5'})

    def test_discover_instances_with_rules_bad_range_rule_param_should_raise_exception(self):
        instance2 = {'id': '52c577679078b9023b3a2c4b', 'uri': 'http://test2', 'version': '2.0'}
        self.mock_class_dao.find.return_value = {'class_name': 'test', 'version': '1.0'}
        self.mock_binding_dao.find_by_class_and_origin.return_value = {
            'class_name': 'test',
           'binding_rules':
           [
            {
             "bindings": [instance2['id']],
             "group_rules": [{'operation': 'range', 'input_context_param': 'uuid', 'value': [1, '200']}]
            }
           ]
         }

        self.assertRaises(GenericServiceError, self.service.get_binding_instance,
                          {'class_name': 'test', 'origin': 'cli', 'uuid': '1'})
        self.assertEquals(0, self.mock_instance_dao.call_count, "instance dao was called")

    def test_discover_instances_with_rules_unsupported_operation_should_raise_exception(self):
        instance2 = {'id': '52c577679078b9023b3a2c4b', 'uri': 'http://test2', 'version': '2.0'}
        self.mock_class_dao.find.return_value = {'class_name': 'class', 'version': '1.0'}
        self.mock_binding_dao.find_by_class_and_origin.return_value = {
            'class_name': 'test',
           'origin': 'cli',
           'binding_rules':
           [
            {
             "bindings": [instance2['id']],
             "group_rules": [{'operation': 'rangio', 'input_context_param': 'uuid', 'value': [1, 200]}]
            }
           ]
         }
        self.assertRaises(GenericServiceError, self.service.get_binding_instance,
                          {'class_name': 'test', 'origin': 'cli', 'uuid': '1'})
        self.assertEquals(0, self.mock_instance_dao.call_count, "instance dao was called")

    def test_discover_instances_with_rules_bad_in_query_param_should_raise_exception(self):
        instance2 = {'id': '52c577679078b9023b3a2c4b', 'uri': 'http://test2', 'version': '2.0'}
        self.mock_class_dao.find.return_value = {'class_name': 'class', 'version': '1.0'}
        self.mock_binding_dao.find_by_class_and_origin.return_value = {
            'class_name': 'test',
                      'origin': 'cli',
                       'binding_rules':
                       [
                        {
                         "bindings": [instance2['id']],
                         "group_rules": [{'operation': 'in', 'input_context_param': 'uuid', 'value': [1, 200]}]
                        }
                       ]
                     }
        self.assertRaises(UnsupportedParameterValueException, self.service.get_binding_instance,
                          {'class_name': 'test', 'origin': 'cli', 'uuid': 'es'})
        self.assertEquals(0, self.mock_instance_dao.call_count, "instance dao was called")

    def test_discover_instances_with_no_rules_matching_should_raise_not_matching(self):
        instance2 = {'id': '52c577679078b9023b3a2c4b', 'uri': 'http://test2', 'version': '2.0'}
        self.mock_class_dao.find.return_value = {'class_name': 'class', 'version': '1.0'}
        self.mock_binding_dao.find_by_class_and_origin.return_value = {
            'class_name': 'test',
           'origin': 'cli',
           'binding_rules':
           [
            {
             "bindings": [instance2['id']],
             "group_rules": [{'operation': 'in', 'input_context_param': 'uuid', 'value': [1, 200]}]
            }
           ]
         }
        with self.assertRaises(NotMatchingRuleException) as cm:
            self.service.get_binding_instance({'class_name': 'test', 'origin': 'cli', 'no-param': 'es'})
        self.assertEquals(0, self.mock_instance_dao.call_count, "instance dao was called")
        self.assertEquals('Resource binding-test-cli does not exist', cm.exception._details)
