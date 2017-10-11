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
from commons.json_schema_validator.schema_reader import SchemaField
from commons.json_schema_validator.schema_reader import SchemaReader
from users.serializers import UserCollectionSerializer


class UserSerializerTests(TestCase):

    def setUp(self):
        super(UserSerializerTests, self).setUp()
        mock_schema_instance = MagicMock(name='mock_schema_instance')
        mock_schema_instance.return_value = [
        SchemaField(name='username', field_type='string', required=True),
        SchemaField(name='password', field_type='string', required=True),
        SchemaField(name='is_admin', field_type='boolean', required=True, default=False)
        ]

        mock_get_schema_fields = MagicMock(name='mock_get_schema')
        mock_get_schema_fields.return_value = mock_schema_instance
        # mock schema instance
        schema_reader = SchemaReader()
        self.patcher_validate = patch.object(schema_reader, 'validate_object')  # @UndefinedVariable
        self.patcher_schema = patch.object(schema_reader,  # @UndefinedVariable
                                        'get_schema_fields', mock_schema_instance)
        self.patcher_schema.start()
        self.patcher_validate.start()

    def tearDown(self):
        self.patcher_schema.stop()
        self.patcher_validate.stop()

    def test_deserialize_user_should_work(self):
        # We need to do import here in order generic patches work
        serializer = UserCollectionSerializer(data={'username': 'user', 'password': 'pass'})
        self.assertEquals(True, serializer.is_valid(), "Serialization invalid")

    def test_deserialize_user_invalid_is_admin_should_work(self):
        # We need to do import here in order generic patches work
        serializer = UserCollectionSerializer(data={'username': 'user', 'password': 'pass', 'is_admin': 'si'})
        self.assertEquals(False, serializer.is_valid(), "Serialization invalid")

    def test_deserialize_user_empty_user_should_give_error_invalid(self):
        # We need to do import here in order generic patches work
        serializer = UserCollectionSerializer(data={'username': '', 'password': 'pass'})
        self.assertEquals(False, serializer.is_valid(), "Serialization invalid")
        self.assertEquals(u"invalid",
                          serializer.errors['username'][0],
                          'Invalid error message')

    def test_deserialize_user_null_user_should_give_required_error(self):
        # We need to do import here in order generic patches work
        serializer = UserCollectionSerializer(data={'password': 'pass'})
        self.assertEquals(False, serializer.is_valid(), "Serialization invalid")
        self.assertEquals(u"required",
                          serializer.errors['username'][0],
                          'Invalid error message')

    def test_deserialize_user_large_user_ne_should_give_invalid_error(self):
        # We need to do import here in order generic patches work
        serializer = UserCollectionSerializer(data={'username': 'a' * 600, 'password': 'pass'})
        self.assertEquals(False, serializer.is_valid(), "Serialization invalid")
        self.assertEquals(u"invalid",
                          serializer.errors['username'][0],
                          'Invalid error message')

    def test_deserialize_user_with_invalid_origins_should_give_error(self):
        serializer = UserCollectionSerializer(data={'username': 'user', 'password': 'pass', 'origins': ["????"]})
        self.assertEquals(False, serializer.is_valid())
        self.assertEquals(u"invalid",
                          serializer.errors['origins'][0],
                          'Invalid error message')
        serializer = UserCollectionSerializer(data={'username': 'user', 'password': 'pass', 'origins': [" tugo"]})
        self.assertEquals(False, serializer.is_valid())
        self.assertEquals(u"invalid",
                          serializer.errors['origins'][0],
                          'Invalid error message')

    def test_deserialize_user_with_invalid_classes_should_give_error(self):
        serializer = UserCollectionSerializer(data={'username': 'user', 'password': 'pass', 'classes': ["????"]})
        self.assertEquals(False, serializer.is_valid())
        self.assertEquals(u"invalid",
                          serializer.errors['classes'][0],
                          'Invalid error message')
        serializer = UserCollectionSerializer(data={'username': 'user', 'password': 'pass', 'classes': [" sms"]})
        self.assertEquals(False, serializer.is_valid())
        self.assertEquals(u"invalid",
                          serializer.errors['classes'][0],
                          'Invalid error message')

    def test_deserialize_user_invalid_username_should_give_error(self):
        # We need to do import here in order generic patches work
        serializer = UserCollectionSerializer(data={'username': 'User.user', 'password': 'pass'})
        self.assertEquals(False, serializer.is_valid(), "Serialization invalid")
        self.assertEquals(u"invalid",
                          serializer.errors['username'][0],
                          'Invalid error message')

    def test_deserialize_user_invalid_is_admin_should_give_error(self):
        # We need to do import here in order generic patches work
        serializer = UserCollectionSerializer(data={'username': 'usera', 'password': 'pass', 'is_admin': 0})
        self.assertEquals(False, serializer.is_valid(), "Serialization invalid")
        self.assertEquals(u"invalid",
                          serializer.errors['is_admin'][0],
                          'Invalid error message')
