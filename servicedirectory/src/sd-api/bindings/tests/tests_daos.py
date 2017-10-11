'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
from pymongo.errors import OperationFailure, DuplicateKeyError
from mock import MagicMock, patch

from commons.test_utils import TestCase
from bindings.daos import BindingDao


class BindingDaoTests(TestCase):
    mock_coll = MagicMock(name='mock_coll')

    @classmethod
    def setUpClass(cls):
        super(BindingDaoTests, cls).setUpClass()
        # Make that instances of class and instances dao point the mocks

        cls.dao = BindingDao()
        # ensure test-test binding is created
        cls.rules = [{
            'bindings': ['endpoint_instance_test'],
            'group_rules': [{'operation': 'eq', 'input_context_param': 'ob', 'value': ['es']},
                {'operation':'eq', 'input_context_param': 'premium', 'value': [True]}]
        }]
        cls.binding_test = {'class_name': 'test', 'origin': 'test', 'binding_rules': cls.rules}
        try:
            cls.binding_test = cls.dao.create(cls.binding_test)
        except DuplicateKeyError:  # for cases where we stop the tests at the middle
            pass

    def test_update_binding_fail_db_should_raise_operation_failure(self):
        binding_new = {
            '_id': self.binding_test['_id'],
            'class_name': 'test',
            'origin': 'test_new',
            'binding_rules': self.rules
        }
        dao_mock = BindingDao()
        # monkey patching daos for the execution of this class
        with patch.object(dao_mock, 'dbcoll', )  as(mock_coll):  # @UndefinedVariable
            mock_coll.update.side_effect = OperationFailure('can not')
            self.assertRaises(OperationFailure, dao_mock.update_binding, binding_new)

    def test_update_binding_duplicated_existing_should_raise_DuplicateKeyError(self):
        binding_new = {
            'class_name': 'test',
            'origin': 'test_new',
            'binding_rules': self.rules
        }
        binding_new = self.dao.create(binding_new)
        binding_new['origin'] = 'test'
        self.assertRaises(DuplicateKeyError, self.dao.update_binding, binding_new)

    def test_update_binding_invalid_id_should_return_false(self):
        binding_2_update = {
            '_id': 'invalid_id',
            'class_name': 'test',
            'origin': 'test_new',
            'binding_rules': self.rules
        }
        self.assertFalse(self.dao.update_binding(binding_2_update))

    def test_delete_binding_invalid_id_should_return_false(self):
        self.assertFalse(self.dao.delete('invalid_id'))

    def test_get_binding_invalid_id_should_return_none(self):
        self.assertFalse(self.dao.find('invalid_id'))
