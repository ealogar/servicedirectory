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
from commons.test_utils import DictMatcher
from users.daos import UserAdminDao
from pymongo.errors import OperationFailure


class UsersDaosTests(TestCase):
    mock_coll = MagicMock(name='mock_coll')

    @classmethod
    def setUpClass(cls):
        super(UsersDaosTests, cls).setUpClass()
        # Make that instances of classes and Instances dao point the mocks
        cls.dao_mock = UserAdminDao()
        cls.dao = UserAdminDao()

        # monkey patching daos for the execution of this class
        cls.patcher_coll = patch.object(cls.dao_mock, 'dbcoll', cls.mock_coll)  # @UndefinedVariable
        cls.patcher_coll.start()

    @classmethod
    def tearDownClass(cls):
        cls.patcher_coll.stop()
        super(UsersDaosTests, cls).tearDownClass()

    def setUp(self):
        super(UsersDaosTests, self).setUp()
        self.mock_coll.reset_mock()
        self.mock_coll.update.reset_mock()

    def test_update_user_fail_db_should_return_false(self):
        self.mock_coll.update.side_effect = OperationFailure('can not')
        self.assertRaises(OperationFailure, self.dao_mock.update,
                          {'classes': ['test'], '_id': 'test', 'password': 'pass'})

        expectUser = DictMatcher({'password': 'pass'}, ['_id'])
        self.mock_coll.update.assert_called_once_with({'_id': 'test'}, expectUser, upsert=False)

    def test_update_user_non_existing_should_return_false(self):
        res = self.dao.update({'classes': ['test'], '_id': 'non-existing-user', 'password': 'pass'})
        self.assertEquals(False, res)
