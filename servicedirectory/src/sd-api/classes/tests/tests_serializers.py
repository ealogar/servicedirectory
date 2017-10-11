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
from bson.objectid import ObjectId
from classes.serializers import ServiceInstanceSerializer, ServiceClassCollectionSerializer,\
    ServiceClassItemSerializer
from commons.json_schema_validator.schema_reader import SchemaReader
from re import match


class InstancesSerializerTests(TestCase):

    def setUp(self):
        super(InstancesSerializerTests, self).setUp()
        mock_schema_instance = MagicMock(name='mock_schema_instance')
        mock_schema_instance.return_value = [
        SchemaField(name='uri', field_type='string', required=True, min_length=1, max_length=2048),
        SchemaField(name='version', field_type='string', required=True, min_length=1, max_length=256),
        SchemaField(name='environment', field_type='string', required=False, min_length=1, max_length=512,
                    default='production'),
        SchemaField(name='class_name', field_type='string', required=True, min_length=1, max_length=512)
        ]

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

    def test_deserialize_instance_should_work(self):
        serializer = ServiceInstanceSerializer(data={'uri': 'url_test', 'version': '1.0', 'environment': 'test',
                                              'class_name': 'test_class'})
        self.assertEquals(True, serializer.is_valid(), "Serialization invalid")

    def test_serialize_valid_instance_should_work(self):
        id_ = ObjectId()
        serializer = ServiceInstanceSerializer({'uri': 'url_test', 'version': '1.0', 'environment': 'test',
                                              'class_name': 'test_class', '_id': id_})
        self.assertEquals(serializer.data['id'], str(id_))

    def test_deserialize_instance_empty_params_should_return_invalid(self):
        serializer = ServiceInstanceSerializer(data={'uri': '', 'version': '1.0', 'environment': 'test',
                                              'class_name': 'test_class'})
        self.assertEquals(False, serializer.is_valid(), "Deserialization invalid")
        self.assertEquals(serializer.errors['uri'][0], 'invalid')

        serializer = ServiceInstanceSerializer(data={'uri': 'url_test', 'version': '', 'environment': 'test',
                                              'class_name': 'test_class'})
        self.assertEquals(False, serializer.is_valid(), "Deserialization invalid")
        self.assertEquals(serializer.errors['version'][0], 'invalid')

        serializer = ServiceInstanceSerializer(data={'uri': 'url_test', 'version': '1.0', 'environment': 'test',
                                              'class_name': ''})
        self.assertEquals(False, serializer.is_valid(), "Deserialization invalid")
        self.assertEquals(serializer.errors['class_name'][0], 'invalid')

    def test_deserialize_instance_null_required_params_should_return_required(self):
        serializer = ServiceInstanceSerializer(data={'version': '1.0', 'environment': 'test',
                                              'class_name': 'test_class'})
        self.assertEquals(False, serializer.is_valid(), "Deserialization invalid")
        self.assertEquals(serializer.errors['uri'][0], 'required')

        serializer = ServiceInstanceSerializer(data={'version': '1.0', 'environment': 'test',
                                              'class_name': 'test_class', 'uri': None})
        self.assertEquals(False, serializer.is_valid(), "Deserialization invalid")
        self.assertEquals(serializer.errors['uri'][0], 'required')

        serializer = ServiceInstanceSerializer(data={'uri': 'url_test', 'environment': 'test',
                                              'class_name': 'test_class'})
        self.assertEquals(False, serializer.is_valid(), "Deserialization invalid")
        self.assertEquals(serializer.errors['version'][0], 'required')

        serializer = ServiceInstanceSerializer(data={'uri': 'url_test', 'version': '1.0', 'environment': 'test'})
        self.assertEquals(False, serializer.is_valid(), "Deserialization invalid")
        self.assertEquals(serializer.errors['class_name'][0], 'required')

    def test_deserialize_instance_large_params_should_return_invalid(self):
        serializer = ServiceInstanceSerializer(data={'uri': 'a' * 2500, 'version': '1.0', 'environment': 'test',
                                              'class_name': 'test_class'})
        self.assertEquals(False, serializer.is_valid(), "Deserialization invalid")
        self.assertEquals(serializer.errors['uri'][0], 'invalid')

        serializer = ServiceInstanceSerializer(data={'uri': 'url_test', 'version': 'v' * 300, 'environment': 'test',
                                              'class_name': 'test_class'})
        self.assertEquals(False, serializer.is_valid(), "Deserialization invalid")
        self.assertEquals(serializer.errors['version'][0], 'invalid')

        serializer = ServiceInstanceSerializer(data={'uri': 'url_test', 'version': '1.0', 'environment': 'test',
                                              'class_name': 'a' * 600})
        self.assertEquals(False, serializer.is_valid(), "Deserialization invalid")
        self.assertEquals(serializer.errors['class_name'][0], 'invalid')

    def test_deserialize_instance_with_attributes_should_work(self):
        serializer = ServiceInstanceSerializer(data={'uri': 'url_test', 'version': '1.0', 'environment': 'test',
                                              'class_name': 'test_class', 'attributes':
                                            {'key': 'keyvalue'}})
        self.assertEquals(True, serializer.is_valid(), "Serialization invalid")

    def test_deserialize_several_instances_with_attributes_should_work(self):
        serializer_lists = [
                        {'uri': 'url_test', 'version': '1.0', 'environment': 'test',
                          'class_name': 'test_class', 'attributes':
                           {'key': 'keyvalue'}},
                        {'uri': 'url_test2', 'version': '1.0', 'environment': 'test',
                          'class_name': 'test_class', 'attributes':
                           {'key_dos': 'keyvalue'}}
                ]

        serializer = ServiceInstanceSerializer(data=serializer_lists, many=True)
        self.assertEquals(True, serializer.is_valid(), "Serialization invalid")
        # Ensure that attributes keys are not included when null data is given
        self.assertTrue('key_dos' not in serializer.data[0]['attributes'], 'key_dos is present in attributes')
        self.assertTrue('key' not in serializer.data[1]['attributes'], 'key is present in attributes')

    def test_deserialize_instance_with_invalid_attributes_should_give_error(self):
        serializer = ServiceInstanceSerializer(data={'uri': 'url_test', 'version': '1.0', 'environment': 'test',
                                              'class_name': 'test_class', 'attributes':
                                            {'key': 1}})
        self.assertEquals(False, serializer.is_valid())
        self.assertEquals("Invalid parameter value: 1",
                          serializer.errors['attributes'][0],
                          'Invalid error message')

    def test_deserialize_instance_with_uppercase_attributes_should_give_error(self):
        serializer = ServiceInstanceSerializer(data={'uri': 'url_test', 'version': '1.0', 'environment': 'test',
                                              'class_name': 'test_class', 'attributes':
                                            {'KEY': '1'}})
        self.assertEquals(False, serializer.is_valid())
        self.assertEquals("Invalid parameter value: KEY",
                          serializer.errors['attributes'][0],
                          'Invalid error message')

    def test_deserialize_instance_with_null_attributes_should_give_error(self):
        serializer = ServiceInstanceSerializer(data={'uri': 'url_test', 'version': '1.0', 'environment': 'test',
                                              'class_name': 'test_class', 'attributes': None
                                            })
        self.assertEquals(False, serializer.is_valid())
        self.assertEquals("Invalid parameter value: null",
                          serializer.errors['attributes'][0],
                          'Invalid error message')

    def test_deserialize_instance_with_bad_format_attributes_should_give_error(self):
        serializer = ServiceInstanceSerializer(data={'uri': 'url_test', 'version': '1.0', 'environment': 'test',
                                              'class_name': 'test_class', 'attributes': 25
                                            })
        self.assertEquals(False, serializer.is_valid())
        self.assertEquals("Invalid parameter value: 25",
                          serializer.errors['attributes'][0],
                          'Invalid error message')

    def test_deserialize_instance_with_wrong_size_attributes_should_give_error(self):
        attributes = dict((str(e), str(e)) for e in range(129))
        serializer = ServiceInstanceSerializer(data={'uri': 'url_test', 'version': '1.0', 'environment': 'test',
                                              'class_name': 'test_class', 'attributes': attributes
                                            })
        self.assertEquals(False, serializer.is_valid())
        self.assertTrue(match("Invalid parameter value: {*",
                          serializer.errors['attributes'][0]))

    def test_deserialize_instance_with_wrong_key_size_attributes_should_give_error(self):
        attributes = {'': 'value'}
        serializer = ServiceInstanceSerializer(data={'uri': 'url_test', 'version': '1.0', 'environment': 'test',
                                              'class_name': 'test_class', 'attributes': attributes
                                            })
        self.assertEquals(False, serializer.is_valid())
        self.assertTrue(match("Invalid parameter value: empty-string",
                          serializer.errors['attributes'][0]))
        attributes = {'k' * 513: 'value'}
        serializer = ServiceInstanceSerializer(data={'uri': 'url_test', 'version': '1.0', 'environment': 'test',
                                              'class_name': 'test_class', 'attributes': attributes
                                            })
        self.assertEquals(False, serializer.is_valid())
        self.assertTrue(match("Invalid parameter value: {0}".format('k' * 513),
                          serializer.errors['attributes'][0]))

    def test_deserialize_instance_with_wrong_value_size_attributes_should_give_error(self):
        attributes = {'kye': ''}
        serializer = ServiceInstanceSerializer(data={'uri': 'url_test', 'version': '1.0', 'environment': 'test',
                                              'class_name': 'test_class', 'attributes': attributes
                                            })
        self.assertEquals(False, serializer.is_valid())
        self.assertTrue(match("invalid",
                          serializer.errors['attributes'][0]['kye'][0]))
        attributes = {'key': 'k' * 513}
        serializer = ServiceInstanceSerializer(data={'uri': 'url_test', 'version': '1.0', 'environment': 'test',
                                              'class_name': 'test_class', 'attributes': attributes
                                            })
        self.assertEquals(False, serializer.is_valid())
        self.assertTrue(match("invalid",
                          serializer.errors['attributes'][0]['key'][0]))

    def test_deserialize_instance_with_bad_format_url_should_give_error(self):
        serializer = ServiceInstanceSerializer(data={'uri': 1, 'version': '1.0', 'environment': 'test',
                                              'class_name': 'test_class'})
        self.assertEquals(False, serializer.is_valid())
        self.assertEquals("invalid",
                          serializer.errors['uri'][0],
                          'Invalid error message')

    def test_deserialize_instance_with_empty_string_environment_should_give_error(self):
        serializer = ServiceInstanceSerializer(data={'uri': "http", 'version': '1.0', 'environment': '',
                                              'class_name': 'test_class'})
        self.assertEquals(False, serializer.is_valid())
        self.assertEquals("invalid",
                          serializer.errors['environment'][0],
                          'Invalid error message')


class ClassesSerializerTests(TestCase):

    def setUp(self):
        super(ClassesSerializerTests, self).setUp()
        mock_schema_instance = MagicMock(name='mock_schema_instance')
        mock_schema_instance.return_value = [
            SchemaField(name='_id', field_type='string', required=True, min_length=1, max_length=512),
            SchemaField(name='description', field_type='string', required=False),
            SchemaField(name='default_version', field_type='string', required=True, min_length=1, max_length=256)
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

    def test_deserialize_class_should_work(self):
        # We need to do import here in order generic patches work
        serializer = ServiceClassCollectionSerializer(data={'class_name': 'class_test', 'default_version': '1.0',
                                                   'description': 'test'})
        self.assertEquals(True, serializer.is_valid(), "Serialization invalid")

    def test_deserialize_class_empty_class_name_should_give_error_invalid(self):
        # We need to do import here in order generic patches work
        serializer = ServiceClassCollectionSerializer(data={'class_name': '', 'version': '1.0', 'description': 'test'})
        self.assertEquals(False, serializer.is_valid(), "Serialization invalid")
        self.assertEquals(u"invalid",
                          serializer.errors['class_name'][0],
                          'Invalid error message')

    def test_deserialize_class_null_class_name_should_give_required_error(self):
        # We need to do import here in order generic patches work
        serializer = ServiceClassCollectionSerializer(data={'default_version': '1.0', 'description': 'test'})
        self.assertEquals(False, serializer.is_valid(), "Serialization invalid")
        self.assertEquals(u"required",
                          serializer.errors['class_name'][0],
                          'Invalid error message')

    def test_deserialize_class_large_user_ne_should_give_invalid_error(self):
        # We need to do import here in order generic patches work
        serializer = ServiceClassCollectionSerializer(data={'class_name': 'a' * 600, 'default_version': '1.0',
                                                   'description': 'test'})
        self.assertEquals(False, serializer.is_valid(), "Serialization invalid")
        self.assertEquals(u"invalid",
                          serializer.errors['class_name'][0],
                          'Invalid error message')

    def test_serialize_class_item_should_return_class_name(self):
        # We need to do import here in order generic patches work
        serializer = ServiceClassItemSerializer({'_id': 'my_class', 'default_version': '1.0',
                                                       'description': 'test'})
        self.assertTrue('class_name' in serializer.data, 'class_name not returned')
