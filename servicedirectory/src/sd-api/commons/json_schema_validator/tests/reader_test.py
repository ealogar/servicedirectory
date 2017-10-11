'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
import unittest
from mock import patch, MagicMock, ANY
from commons.exceptions import GenericServiceError
from commons.json_schema_validator.schema_reader import SchemaReader,\
    SchemaField
from jsonschema import ValidationError
import os
from django.test.utils import override_settings
from commons.singleton import Singleton
path_properties = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schemas')

json_mock = MagicMock(name='jsonMock')


class SchemaReaderTest(unittest.TestCase):

    right_model = "UserModel"

    @override_settings(JSON_SCHEMAS_FOLDER=path_properties)
    def setUp(self):
        try:
            SchemaReader._instances[SchemaReader] = None  # @UndefinedVariable
            del SchemaReader._instances[SchemaReader]  # @UndefinedVariable
        except Exception as e:
            print str(e)
        self.schemaReader = SchemaReader()

    def test_schema_reader_should_be_a_singleton(self):
        schemaReader2 = SchemaReader()
        self.assertEquals(id(self.schemaReader), id(schemaReader2))

    def test_right_json_schema_should_load_file(self):
        self.schemaReader = SchemaReader()
        schema = self.schemaReader.get_schema('UserModel')
        self.assertEquals('UserModel', schema['title'])
        self.assertEquals('object', schema['type'])

    def test_init_schema_not_json_schemas_config_should_exit(self):
        Singleton._instances.pop(SchemaReader, None)

        class SettingsMock(object):
            pass
        mock_settings = SettingsMock()
        with patch('commons.json_schema_validator.schema_reader.settings', new=mock_settings) as mock_settings:
            self.assertRaises(GenericServiceError, SchemaReader)

    def test_get_unexisting_json_schema_should_launch_GenericServiceError(self):
        # only right schema loaded
        self.assertEquals(3, len(self.schemaReader._schemas))

        self.assertRaises(GenericServiceError, lambda: self.schemaReader.get_schema('BadUserModel'))

    @patch('commons.json_schema_validator.schema_reader.json', json_mock)
    def test_bad_json_schema_should_load_file_and_launch_GenericServiceError(self):
        # only right schema loaded
        schemaReader = SchemaReader()
        self.assertEquals(3, len(self.schemaReader._schemas))
        json_doc = '{"user":"asdasd", "other_property":"asdasd"}'
        self.assertRaises(GenericServiceError, lambda: schemaReader.validate_json_document(json_doc,
                                                                                                   'BadUserModel'))
        json_mock.loads.assert_called_once_with(ANY)

    def test_right_json_string_should_return_void(self):
        schemaReader = SchemaReader()
        json_doc = '{"user":"asdasd", "password":"asdasd"}'
        schemaReader.validate_json_document(json_doc, self.right_model)

    def test_bad_field_json_string_should_raise_validationerror(self):
        schemaReader = SchemaReader()
        json_doc = '{"user":"asdasd", "other_property":"asdasd"}'
        self.assertRaises(ValidationError,
                          lambda: schemaReader.validate_json_document(json_doc, self.right_model))

    def test_bad_type_json_string_should_raise_validationerror(self):
        schemaReader = SchemaReader()
        json_doc = '{"user":"asdasd", "password":12}'
        self.assertRaises(ValidationError,
                          lambda: schemaReader.validate_json_document(json_doc, self.right_model))

    def test_right_object_should_return_void(self):
        schemaReader = SchemaReader()
        json_obj = {"user": "name", "password": "asdasd"}
        schemaReader.validate_object(json_obj, self.right_model)

    def test_bad_object_should_return_raise_validationerror(self):
        schemaReader = SchemaReader()
        json_obj = {"user": "name", "other_property": "asdasd"}
        self.assertRaises(ValidationError,
                          lambda: schemaReader.validate_object(json_obj, self.right_model))

    def test_get_fields_from_object_should_return_valid_list_SchemaField(self):
        schemaReader = SchemaReader()
        schema_fields = schemaReader.get_schema_fields('OptionalProperties')
        self.assertEquals(4, len(schema_fields), "Not all fields were recovered")
        for expected_field in [SchemaField(name='obi', field_type='string', required=False),
                             SchemaField(name='oba', field_type='string', required=False),
                             SchemaField(name='user', field_type='string', required=True),
                             SchemaField(name='password', field_type='string', required=True)]:
            for returned_field in schema_fields:
                if expected_field.name == returned_field.name:
                    self.assertEquals(expected_field.required, returned_field.required,
                                      "Invalid required recovered for {0}".format(returned_field))

    def test_get_several_fields_from_object_should_return_different_SchemaField(self):
        schemaReader = SchemaReader()
        schema_fields = schemaReader.get_schema_fields('SeveralFieldsModel')
        self.assertEquals(4, len(schema_fields), "Not all fields were recovered")
        for expected_field in [SchemaField(name='mytext', field_type='string', required=True,
                                           min_length=1, max_length=10),
                             SchemaField(name='mynum', field_type='integer', required=True,
                                         min_value=0, max_value=100),
                             SchemaField(name='mybool', field_type='boolean', required=True),
                             SchemaField(name='mydefault', field_type='string', required=True,
                                         default='default_value')]:
            for returned_field in schema_fields:
                if expected_field.name == returned_field.name:
                    self.assertEquals(expected_field.required, returned_field.required,
                                      "Invalid required recovered for {0}".format(returned_field.name))
