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
from commons.exceptions import NotFoundException, GenericServiceError
from users.services import UserAdminService
from commons.test_utils import DictMatcher
from rest_framework.exceptions import PermissionDenied


class UsersServiceTests(TestCase):
    mock_dao = MagicMock(name='mock_dao')
    mock_classes_dao = MagicMock(name='mock_classes_dao')

    @classmethod
    def setUpClass(cls):
        super(UsersServiceTests, cls).setUpClass()
        # Make that instances of classes and Instances dao point the mocks
        cls.service = UserAdminService()

        # monkey patching daos for the execution of this class
        cls.patcher_dao = patch.object(cls.service, 'dao', cls.mock_dao)  # @UndefinedVariable
        cls.patcher_class_dao = patch.object(cls.service, 'classes_dao', cls.mock_classes_dao)  # @UndefinedVariable
        cls.patcher_dao.start()
        cls.patcher_class_dao.start()

    @classmethod
    def tearDownClass(cls):
        cls.patcher_dao.stop()
        cls.patcher_class_dao.stop()
        super(UsersServiceTests, cls).tearDownClass()

    def setUp(self):
        super(UsersServiceTests, self).setUp()
        self.mock_dao.reset_mock()
        self.mock_dao.update.reset_mock()
        self.mock_dao.delete.reset_mock()

    def test_get_user_non_existing_should_raiseNotFound(self):
        self.mock_dao.find.return_value = None
        self.assertRaises(NotFoundException, self.service.get_user, 'test')
        self.mock_dao.find.assert_called_once_with('test')

    def test_update_user_fail_db_should_raiseGenericException(self):
        self.mock_dao.update.return_value = False
        self.mock_classes_dao.find.return_value = {'class_name': 'test'}
        self.assertRaises(GenericServiceError, self.service.update, {'classes': ['test'],
                                                    '_id': 'test', 'password': 'pass'}, 'test-admin')
        self.assertEquals(0, self.mock_dao.find.call_count, "find was called")
        expectUser = DictMatcher({'_id': 'test', 'password': 'pass'}, [])
        self.mock_dao.update.assert_called_once_with(expectUser)

    def test_delete_user_fail_db_should_raiseGenericException(self):
        self.mock_dao.find.return_value = {'_id': 'test', 'password': 'pass'}
        self.mock_dao.delete.return_value = False
        self.assertRaises(GenericServiceError, self.service.delete, 'test', 'test-admin')
        self.mock_dao.find.assert_called_once_with('test')
        self.mock_dao.delete.assert_called_once_with('test')

    def test_delete_user_admin_himself_should_raise_PermissionDenied(self):
        self.mock_dao.find.return_value = {'_id': 'test', 'password': 'pass'}
        self.mock_dao.delete.return_value = True
        self.assertRaises(PermissionDenied, self.service.delete, 'test', 'test')
        self.mock_dao.find.assert_called_once_with('test')
        self.assertEquals(0, self.mock_dao.delete.call_count, "Mock dao shouldnt be called")
