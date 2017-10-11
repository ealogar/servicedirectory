
from unittest import TestCase
from mock import MagicMock, patch
from commons.serializers import generate_location_header, get_first_error,\
    serialize_to_response, SchemaSerializer
from rest_framework.response import Response
from contextlib import nested
from commons.json_schema_validator.schema_reader import SchemaReader,\
    SchemaField


class CommonsSerializersTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super(CommonsSerializersTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # Access Singleton and remove ServiceInstanceService singleton
        super(CommonsSerializersTest, cls).tearDownClass()

    def setUp(self):
        pass

    def test_generate_location_header_invalid_reverse_fields_should_return_empty_dict(self):

        with patch('commons.serializers.reverse') as reverse_mock:
            reverse_mock.side_effect = Exception
            serializer = MagicMock(name='serializer_mock')
            request = MagicMock(name='request_mock')
            header = generate_location_header(serializer, request)
            self.assertEquals({}, header)

    def test_get_first_error_return_nested_error(self):
        errors = {u'mykey': [{'subkey': [u'my_error']}]}
        input_data = {'mykey': {'subkey': 'subvalue'}}
        (key, value, error) = get_first_error(errors, input_data)
        self.assertEquals("subkey", key, "Unexpected key returned")
        self.assertEquals("subvalue", value, "Unexpected value returned")
        self.assertEquals("my_error", error, "Unexpected excpetion returned")

    def test_get_first_error_nested_array_serializer_return_nested_error(self):
        errors = {u'mykey': [{}, {'subkey': [u'my_error']}]}
        input_data = {'mykey': [{'subkey': 25}, {'subkey': 'subvalue'}]}
        (key, value, error) = get_first_error(errors, input_data)
        self.assertEquals("subkey", key, "Unexpected key returned")
        self.assertEquals("subvalue", value, "Unexpected value returned")
        self.assertEquals("my_error", error, "Unexpected excpetion returned")

    def test_get_first_error_nested_array_serializer_invalid_return_nested_error(self):
        errors = {u'mykey': [{'subkey': [{'non_field_errors': ['non valid object']}]}]}
        input_data = {'mykey': {'subkey': {'think': 'value'}}}
        (key, value, error) = get_first_error(errors, input_data)
        self.assertEquals("subkey", key, "Unexpected key returned")
        self.assertEquals({'think': 'value'}, value, "Unexpected value returned")
        self.assertEquals("invalid", error, "Unexpected excpetion returned")

    def test_get_first_error_bad_serializer_errors_should_return_error(self):
        errors = 'non valid object'
        input_data = {'mykey': {'subkey': {'think': 'value'}}}
        (key, value, error) = get_first_error(errors, input_data)
        self.assertEquals("", key, "Unexpected key returned")
        self.assertEquals('', value, "Unexpected value returned")
        self.assertEquals(unicode(errors), error, "Unexpected excpetion returned")

    def test_serializer_response_status_201_should_return_same_response_with_location(self):
        view_mock = MagicMock(name='view_mock')
        request_mock = MagicMock(name='request_mock')

        resp = Response({'data': 'my_data'}, status=201, headers={})

        def return_response(view, request):
            return resp

        # apply decorator
        return_response = serialize_to_response()(return_response)
        with patch('commons.serializers.reverse') as reverse_mock:
            reverse_mock.return_value = 'http://test.test'
            obj = return_response(view_mock, request_mock)
            self.assertEquals('my_data', obj.data['data'], 'object was not same')
            self.assertEquals(1, len(obj.data), 'object was not same')
            self.assertEquals('http://test.test', obj['Location'], 'Location header was not included')

    def test_serializer_with_max_integer_values_should_work(self):
        # mock schema instance
        schema_reader = SchemaReader()

        with nested(patch.object(schema_reader, 'validate_object'),  # @UndefinedVariable
            patch.object(schema_reader, 'get_schema_fields', )) as(validate_mock, mock_schema_instance):  # @UndefinedVariable
            mock_schema_instance.return_value = [
                    SchemaField(name='key1', field_type='integer', required=True, min_value=1, max_value=500),
                    SchemaField(name='keycustom', field_type='custom_obj', required=True)
                    ]

            class IntegersSerializers(SchemaSerializer):

                class Meta():
                    schema = 'schemaMock'

            serializer = IntegersSerializers(data={'key1': 12, 'keycustom': 'test'})
            self.assertTrue(serializer.is_valid())

    def test_schema_serializer_without_schema_should_raise_exception(self):
        class TestSerializer(SchemaSerializer):
            class Meta():
                model = 'model_test'

        self.assertRaises(AttributeError, TestSerializer)
