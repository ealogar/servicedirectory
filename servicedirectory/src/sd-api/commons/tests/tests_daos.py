
from unittest import TestCase
from commons.daos import BaseDao, MongoConnection
from pymongo.errors import AutoReconnect, ConnectionFailure
from mock import MagicMock, patch, call, ANY
from commons.test_utils import DictMatcher
from commons.singleton import Singleton
from contextlib import nested
from commons.exceptions import GenericServiceError


class DaoTest(BaseDao):
    coll = 'test-coll'


class BaseDaoTest(TestCase):
    mock_connection = MagicMock(name='mock_connection')
    mock_col = MagicMock(name='mock_col')

    @classmethod
    def setUpClass(cls):
        super(BaseDaoTest, cls).setUpClass()
        cls.dao = DaoTest()

        # monkey patching MongoConnection for the execution of this class
        cls.patcher_connection = patch.object(cls.dao, 'dbconn', cls.mock_connection)  # @UndefinedVariable
        cls.patch_col = patch.object(cls.dao, 'dbcoll', cls.mock_col)  # @UndefinedVariable
        cls.patch_sleep = patch('commons.decorators.sleep')
        cls.patcher_connection.start()
        cls.patch_col.start()
        cls.patch_sleep.start()
        # Monkey patching time module

    @classmethod
    def tearDownClass(cls):
        Singleton._instances.pop(MongoConnection, None)
        cls.patcher_connection.stop()
        cls.patch_col.stop()
        cls.patch_sleep.stop()
        # Access Singleton and remove ServiceInstanceService singleton
        super(BaseDaoTest, cls).tearDownClass()

    def setUp(self):
        self.mock_col.reset_mock()
        self.mock_col.find_one.side_effect = None
        self.mock_connection.reset_mock()

    def test_autoreconnect_in_base_dao_should_do_retries_and_return(self):
        self.mock_col.find_one.side_effect = (AutoReconnect, {'_id': 'id_test', 'key': 'example'})
        res = self.dao.find('id_test')
        self.assertEquals('id_test', res['_id'], 'not returned element')
        self.mock_col.find_one.assert_has_calls([call(DictMatcher({'_id': 'id_test'})),
                                                 call(DictMatcher({'_id': 'id_test'}))], False)
        self.assertEquals(2,  self.mock_col.find_one.call_count, 'find_one was not called 3 times')

    def test_autoreconnect_in_base_dao_should_do_retries_and_fail_permanently(self):
        self.mock_col.find_one.side_effect = AutoReconnect
        self.assertRaises(Exception, self.dao.find, 'id_test')
        self.mock_col.find_one.assert_has_calls([call(DictMatcher({'_id': 'id_test'})),
                                                 call(DictMatcher({'_id': 'id_test'})),
                                                 call(DictMatcher({'_id': 'id_test'}))], False)

    def test_BaseDao_cannot_be_extended_without_coll(self):
        self.assertRaises(NotImplementedError, BaseDao)

    def test_init_mongo_connection_some_rs_down_should_give_warning(self):
        Singleton._instances.pop(MongoConnection, None)
        with nested(patch('commons.daos.MongoClient'), patch('commons.daos.logger')) as(MongoClientMock, loggerMock):
            MongoClientMock.side_effect = AutoReconnect
            MongoConnection()
            loggerMock.warning.assert_called_once_with('It has not been possible to connect to all the hosts %s', ANY)

    def test_init_mongo_connection_all_rs_down_should_give_error_and_exist(self):
        Singleton._instances.pop(MongoConnection, None)
        with nested(patch('commons.daos.MongoClient'), patch('commons.daos.logger'),
                    patch('sys.exit')) as(MongoClientMock, loggerMock, exitMock):
            MongoClientMock.side_effect = ConnectionFailure
            self.assertRaises(GenericServiceError, MongoConnection)
            loggerMock.critical.assert_called_once_with(
                            'It has not been possible to start the connection to the hosts %s', ANY)
