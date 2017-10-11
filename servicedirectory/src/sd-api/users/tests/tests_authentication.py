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
from mock import patch, ANY, MagicMock
from users.authentication import BasicMongoAuthentication
from contextlib import nested
from commons.singleton import Singleton
from commons.exceptions import NotFoundException
from commons.test_utils import DictMatcher


class AuthenticationTests(TestCase):

    @classmethod
    def tearDownClass(cls):
        Singleton._instances.pop(BasicMongoAuthentication, None)

    def test_init_basic_authentication_no_credentials_settings_should_write_error_log(self):

        class SettingsMock(object):
            pass
        Singleton._instances.pop(BasicMongoAuthentication, None)
        mock_settings = SettingsMock()
        with nested(
             patch('users.authentication.UserAdminService'),
             patch('users.authentication.settings', new=mock_settings),
             patch('users.authentication.logger')) as(mock_user_admin, mock_settings, mock_logger):
            BasicMongoAuthentication()
            mock_logger.error.assert_called_once_with(ANY)
            self.assertEquals(0, mock_user_admin.get_user.call_count, 'get_user called and it shouldn')

    def test_init_basic_authentication_no_user_created_should_create_user(self):

        Singleton._instances.pop(BasicMongoAuthentication, None)
        with nested(
             patch('users.authentication.UserAdminService'),
             patch('users.authentication.logger')) as(mock_user_admin, mock_logger):
            user_admin_instance = MagicMock(name='user_admin_instance')
            mock_user_admin.return_value = user_admin_instance
            user_admin_instance.get_user.side_effect = NotFoundException('not found')
            BasicMongoAuthentication()
            self.assertEquals(0, mock_logger.error.call_count, 'error log generated and it shouldn')
            user_admin_instance.get_user.assert_called_once_with('admin')
            user_expected = DictMatcher({'_id': 'admin', 'password': 'admin', 'is_admin': True}, [])
            user_admin_instance.create.assert_called_once_with(user_expected)

    def test_init_basic_authentication_no_user_created_fail_creation_should_write_log(self):

        Singleton._instances.pop(BasicMongoAuthentication, None)
        with nested(
             patch('users.authentication.UserAdminService'),
             patch('users.authentication.logger')) as(mock_user_admin, mock_logger):
            user_admin_instance = MagicMock(name='user_admin_instance')
            mock_user_admin.return_value = user_admin_instance
            user_admin_instance.get_user.side_effect = NotFoundException('not found')
            user_admin_instance.create.side_effect = Exception('can not')
            BasicMongoAuthentication()

            user_admin_instance.get_user.assert_called_once_with('admin')
            user_expected = DictMatcher({'_id': 'admin', 'password': 'admin', 'is_admin': True}, [])
            user_admin_instance.create.assert_called_once_with(user_expected)
            mock_logger.error.assert_called_once_with(ANY, ANY)

    def test_authenticate_corrupted_user_should_write_log_and_raise_exception(self):

        basic_auth = BasicMongoAuthentication()
        with nested(patch.object(basic_auth, 'service'),  # @UndefinedVariable
                    patch('users.authentication.logger'),
                    patch('users.authentication.check_password')) as(service_mock, mock_logger, check_password_mock):
            check_password_mock.return_value = True
            service_mock.get_user.return_value = {'_id': 'admin', 'is_staff': True, 'password': 'admin'}
            self.assertRaises(KeyError, basic_auth.authenticate_credentials, 'admin', 'admin')

            mock_logger.error.assert_called_once_with(ANY, ANY)
