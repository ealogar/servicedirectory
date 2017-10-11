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
from bindings.serializers import BindingsSerializer
from commons.json_schema_validator.schema_reader import SchemaReader


class BindingSerializerTests(TestCase):

    def setUp(self):
        mock_schema_instance = MagicMock(name='mock_schema_instance')
        mock_schema_instance.return_value = [
            SchemaField(name='origin', field_type='string', required=True, min_length=1),
            SchemaField(name='class_name', field_type='string', required=True, min_length=1)
        ]
        # mock singleton schema
        schema_reader = SchemaReader()
        self.patcher_validate = patch.object(schema_reader, 'validate_object')  # @UndefinedVariable
        self.patcher_schema = patch.object(schema_reader,  # @UndefinedVariable
                                        'get_schema_fields', mock_schema_instance)
        self.patcher_schema.start()
        self.patcher_validate.start()

    def tearDown(self):
        self.patcher_schema.stop()
        self.patcher_validate.stop()

    def test_deserialize_binding_should_work(self):
        # We need to do import here in order generic patches work
        rules = {
                  'class_name': 'cli',
                  'origin': 'test',
                  'binding_rules':
                  [
                     {
                       "bindings": ["51c577679078b9023b3a2c4b"],
                       "group_rules": [{'operation': 'eq', 'input_context_param': 'ob', 'value': ['es']},
                                       {'operation': 'range', 'input_context_param': 'uuid', 'value': [1, 20]}]
                      }
                  ]
                }
        serializer = BindingsSerializer(data=rules)
        self.assertEquals(True, serializer.is_valid(), "Deserialization invalid")
        des_object = serializer.object
        self.assertEquals('cli', des_object['class_name'])
        self.assertEquals('test', des_object['origin'])

    def test_deserialize_binding_without_group_rules_should_work(self):
        # We need to do import here in order generic patches work
        rules = {
                  'class_name': 'cli',
                  'origin': 'test',
                  'binding_rules':
                  [
                     {
                       "bindings": ["51c577679078b9023b3a2c4b"]
                      }
                  ]
                }
        serializer = BindingsSerializer(data=rules)
        self.assertEquals(True, serializer.is_valid(), "Deserialization invalid")
        des_object = serializer.object
        self.assertEquals('cli', des_object['class_name'])
        self.assertEquals('test', des_object['origin'])

    def test_deserialize_binding_max_size_binding_id_should_fail(self):
        # We need to do import here in order generic patches work
        rules = {
                  'class_name': 'cli',
                  'origin': 'test',
                  'binding_rules':
                  [
                     {
                       "bindings": ["51c577679078b9023b3a2c4b51c577679078b9023b3a2c4b51c577679078b902"],
                       "group_rules": [{'operation': 'eq', 'input_context_param': 'ob', 'value': ['es']},
                                       {'operation': 'range', 'input_context_param': 'uuid', 'value': [1, 20]}]
                      }
                  ]
                }
        serializer = BindingsSerializer(data=rules)
        self.assertEquals(False, serializer.is_valid(), "Deserialization invalid")
        self.assertEquals('invalid', serializer.errors['binding_rules'][0]['bindings'][0])

    def test_deserialize_binding_invalis_size_values_should_fail(self):
        # We need to do import here in order generic patches work
        rules = {
                  'class_name': 'cli',
                  'origin': 'test',
                  'binding_rules':
                  [
                     {
                       "bindings": ["51c577679078b9023b3a2c4b"],
                       "group_rules": [{'operation': 'eq', 'input_context_param': 'ob',
                                        'value': map(lambda x: 'es', range(129))},
                                       {'operation': 'range', 'input_context_param': 'uuid', 'value': [1, 20]}]
                      }
                  ]
                }
        serializer = BindingsSerializer(data=rules)
        self.assertEquals(False, serializer.is_valid(), "Deserialization invalid")
        self.assertEquals('invalid', serializer.errors['binding_rules'][0]['group_rules'][0]['value'][0])

    def test_deserialize_binding_invalid_value_values_should_fail(self):
        # We need to do import here in order generic patches work
        rules = {
                  'class_name': 'cli',
                  'origin': 'test',
                  'binding_rules':
                  [
                     {
                       "bindings": ["51c577679078b9023b3a2c4b"],
                       "group_rules": [{'operation': 'eq', 'input_context_param': 'ob',
                                        'value': 12},
                                       {'operation': 'range', 'input_context_param': 'uuid', 'value': [1, 20]}]
                      }
                  ]
                }
        serializer = BindingsSerializer(data=rules)
        self.assertEquals(False, serializer.is_valid(), "Deserialization invalid")
        self.assertEquals('invalid', serializer.errors['binding_rules'][0]['group_rules'][0]['value'][0])

    def test_deserialize_binding_non_ascii_characters_should_work(self):
        # We need to do import here in order generic patches work
        rules = {
                  'class_name': 'cli',
                  'origin': 'test',
                  'binding_rules':
                  [
                     {
                       "bindings": ["51c577679078b9023b3a2c4b"],
                       "group_rules": [{'operation': 'eq', 'input_context_param': 'ob', 'value': ['es\u00f1']},
                                       {'operation': 'range', 'input_context_param': 'uuid', 'value': [1, 20]}]
                      }
                  ]
                }
        serializer = BindingsSerializer(data=rules)
        self.assertEquals(True, serializer.is_valid(), "Deserialization invalid")
        des_object = serializer.object
        self.assertEquals('cli', des_object['class_name'])
        self.assertEquals('test', des_object['origin'])

    def test_deserialize_binding_no_mandatory_params_should_give_error(self):
        # We need to do import here in order generic patches work
        rules = {
                  'class_name': 'cli',
                  'origin': 'test',
                  'binding_rules':
                  [
                     {
                       "bindings": ["51c577679078b9023b3a2c4b"],
                       "group_rules": [{'operation': 'eq', 'input_context_param': 'ob', 'value': ['es']},
                                       {'operation': 'range', 'input_context_param': 'uuid', 'value': [1, 20]}]
                      }
                  ]
                }
        class_name = rules.pop('class_name')
        serializer = BindingsSerializer(data=rules)
        self.assertEquals(False, serializer.is_valid(), "Deserialization invalid")
        self.assertEquals('required', serializer.errors['class_name'][0], 'Invalid error message')
        rules.pop('origin')
        rules['class_name'] = class_name
        serializer = BindingsSerializer(data=rules)
        self.assertEquals(False, serializer.is_valid(), "Deserialization invalid")
        self.assertEquals('required', serializer.errors['origin'][0], 'Invalid error message')

    def test_deserialize_binding_upper_case_input_params_should_give_error(self):
        # We need to do import here in order generic patches work
        rules = {
                  'class_name': 'cli',
                  'origin': 'test',
                  'binding_rules':
                  [
                     {
                       "bindings": ["51c577679078b9023b3a2c4b"],
                       "group_rules": [{'operation': 'eq', 'input_context_param': 'OB', 'value': ['es']}]
                      }
                  ]
                }
        serializer = BindingsSerializer(data=rules)
        self.assertEquals(False, serializer.is_valid())
        self.assertEquals('Invalid parameter value: OB',
                          serializer.errors['binding_rules'][0]['group_rules'][0]['input_context_param'][0],
                          'Invalid error message')

    def test_deserialize_binding_invalid_input_params_should_give_error(self):
        # We need to do import here in order generic patches work
        rules = {
                  'class_name': 'cli',
                  'origin': 'test',
                  'binding_rules':
                  [
                     {
                       "bindings": ["51c577679078b9023b3a2c4b"],
                       "group_rules": [{'operation': 'eq', 'input_context_param': 'ob.oba', 'value': ['es']}]
                      }
                  ]
                }
        serializer = BindingsSerializer(data=rules)
        self.assertEquals(False, serializer.is_valid())
        self.assertEquals("Invalid parameter value: ob.oba",
                          serializer.errors['binding_rules'][0]['group_rules'][0]['input_context_param'][0],
                          'Invalid error message')

    def test_deserialize_binding_class_name_input_params_should_give_error(self):
        # We need to do import here in order generic patches work
        rules = {
                  'class_name': 'cli',
                  'origin': 'test',
                  'binding_rules':
                  [
                     {
                       "bindings": ["51c577679078b9023b3a2c4b"],
                       "group_rules": [{'operation': 'eq', 'input_context_param': 'class_name', 'value': ['es']}]
                      }
                  ]
                }
        serializer = BindingsSerializer(data=rules)
        self.assertEquals(False, serializer.is_valid())
        self.assertEquals("Invalid parameter value: class_name",
                          serializer.errors['binding_rules'][0]['group_rules'][0]['input_context_param'][0],
                          'Invalid error message')

    def test_deserialize_binding_origin_as_input_params_should_give_error(self):
        # We need to do import here in order generic patches work
        rules = {
                  'class_name': 'cli',
                  'origin': 'test',
                  'binding_rules':
                  [
                     {
                       "bindings": ["51c577679078b9023b3a2c4b"],
                       "group_rules": [{'operation': 'eq', 'input_context_param': 'origin', 'value': ['es']}]
                      }
                  ]
                }
        serializer = BindingsSerializer(data=rules)
        self.assertEquals(False, serializer.is_valid())
        self.assertEquals("Invalid parameter value: origin",
                          serializer.errors['binding_rules'][0]['group_rules'][0]['input_context_param'][0],
                          'Invalid error message')

    def test_deserialize_binding_range_short_should_give_error(self):
        # We need to do import here in order generic patches work
        rules = {
                  'class_name': 'cli',
                  'origin': 'test',
                  'binding_rules':
                  [
                     {
                       "bindings": ["51c577679078b9023b3a2c4b"],
                       "group_rules": [{'operation': 'range', 'input_context_param': 'ob', 'value': [1]}]
                      }
                  ]
                }
        serializer = BindingsSerializer(data=rules)
        self.assertEquals(False, serializer.is_valid())
        self.assertEquals("Invalid parameter value: [1]",
                          serializer.errors['binding_rules'][0]['group_rules'][0]['value'][0],
                          'Invalid error message')

    def test_deserialize_binding_range_invalid_types_should_give_error(self):
        # We need to do import here in order generic patches work
        rules = {
                  'class_name': 'cli',
                  'origin': 'test',
                  'binding_rules':
                  [
                     {
                       "bindings": ["51c577679078b9023b3a2c4b"],
                       "group_rules": [{'operation': 'range', 'input_context_param': 'ob', 'value': [1, 3.5]}]
                      }
                  ]
                }
        serializer = BindingsSerializer(data=rules)
        self.assertEquals(False, serializer.is_valid())
        self.assertEquals("Invalid parameter value: [1, 3.5]",
                          serializer.errors['binding_rules'][0]['group_rules'][0]['value'][0],
                          'Invalid error message')

    def test_deserialize_binding_range_same_values_should_give_error(self):
        # We need to do import here in order generic patches work
        rules = {
                  'class_name': 'cli',
                  'origin': 'test',
                  'binding_rules':
                  [
                     {
                       "bindings": ["51c577679078b9023b3a2c4b"],
                       "group_rules": [{'operation': 'range', 'input_context_param': 'ob', 'value': [1, 1]}]
                      }
                  ]
                }
        serializer = BindingsSerializer(data=rules)
        self.assertEquals(False, serializer.is_valid())
        self.assertEquals("Invalid parameter value: [1, 1]",
                          serializer.errors['binding_rules'][0]['group_rules'][0]['value'][0],
                          'Invalid error message')

    def test_deserialize_binding_range_invalid_values_should_give_error(self):
        # We need to do import here in order generic patches work
        rules = {
                  'class_name': 'cli',
                  'origin': 'test',
                  'binding_rules':
                  [
                     {
                       "bindings": ["51c577679078b9023b3a2c4b"],
                       "group_rules": [{'operation': 'range', 'input_context_param': 'ob', 'value': [100, 1]}]
                      }
                  ]
                }
        serializer = BindingsSerializer(data=rules)
        self.assertEquals(False, serializer.is_valid())
        self.assertEquals("Invalid parameter value: [100, 1]",
                          serializer.errors['binding_rules'][0]['group_rules'][0]['value'][0],
                          'Invalid error message')

    def test_deserialize_binding_in_different_types_should_give_error(self):
        # We need to do import here in order generic patches work
        rules = {
                  'class_name': 'cli',
                  'origin': 'test',
                  'binding_rules':
                  [
                     {
                       "bindings": ["51c577679078b9023b3a2c4b"],
                       "group_rules": [{'operation': 'in', 'input_context_param': 'ob', 'value': ["es", 1]}]
                      }
                  ]
                }
        serializer = BindingsSerializer(data=rules)
        self.assertEquals(False, serializer.is_valid())
        self.assertEquals("Invalid parameter value: 1",
                          serializer.errors['binding_rules'][0]['group_rules'][0]['value'][0],
                          'Invalid error message')

    def test_deserialize_binding_in_repeated_values_should_give_error(self):
        # We need to do import here in order generic patches work
        rules = {
                  'class_name': 'cli',
                  'origin': 'test',
                  'binding_rules':
                  [
                     {
                       "bindings": ["51c577679078b9023b3a2c4b"],
                       "group_rules": [{'operation': 'in', 'input_context_param': 'ob', 'value': ["es", "es"]}]
                      }
                  ]
                }
        serializer = BindingsSerializer(data=rules)
        self.assertEquals(False, serializer.is_valid())
        self.assertEquals("Invalid parameter value: ['es', 'es']",
                          serializer.errors['binding_rules'][0]['group_rules'][0]['value'][0])

    def test_deserialize_binding_in_empty_values_should_give_error(self):
        # We need to do import here in order generic patches work
        rules = {
                  'class_name': 'cli',
                  'origin': 'test',
                  'binding_rules':
                  [
                     {
                       "bindings": ["51c577679078b9023b3a2c4b"],
                       "group_rules": [{'operation': 'in', 'input_context_param': 'ob', 'value': ["", "es"]}]
                      }
                  ]
                }
        serializer = BindingsSerializer(data=rules)
        self.assertEquals(False, serializer.is_valid())
        self.assertEquals(u'invalid', serializer.errors['binding_rules'][0]['group_rules'][0]['value'][0],
                          'Invalid error message')

    def test_deserialize_binding_regex_several_values_should_give_error(self):
        # We need to do import here in order generic patches work
        rules = {
                  'class_name': 'cli',
                  'origin': 'test',
                  'binding_rules':
                  [
                     {
                       "bindings": ["51c577679078b9023b3a2c4b"],
                       "group_rules": [{'operation': 'regex', 'input_context_param': 'ob', 'value': ["es", "es"]}]
                      }
                  ]
                }
        serializer = BindingsSerializer(data=rules)
        self.assertEquals(False, serializer.is_valid())
        self.assertEquals("Invalid parameter value: ['es', 'es']",
                          serializer.errors['binding_rules'][0]['group_rules'][0]['value'][0],
                          'Invalid error message')

    def test_deserialize_binding_regex_invalid_should_give_error(self):
        # We need to do import here in order generic patches work
        rules = {
                  'class_name': 'cli',
                  'origin': 'test',
                  'binding_rules':
                  [
                     {
                       "bindings": ["51c577679078b9023b3a2c4b"],
                       "group_rules": [{'operation': 'regex', 'input_context_param': 'ob', 'value': ["*"]}]
                      }
                  ]
                }
        serializer = BindingsSerializer(data=rules)
        self.assertEquals(False, serializer.is_valid())
        self.assertEquals("Invalid parameter value: ['*']",
                          serializer.errors['binding_rules'][0]['group_rules'][0]['value'][0])

    def test_deserialize_binding_eq_several_values_should_give_error(self):
        # We need to do import here in order generic patches work
        rules = {
                  'class_name': 'cli',
                  'origin': 'test',
                  'binding_rules':
                  [
                     {
                       "bindings": ["51c577679078b9023b3a2c4b"],
                       "group_rules": [{'operation': 'eq', 'input_context_param': 'ob', 'value': ["es", "es"]}]
                      }
                  ]
                }
        serializer = BindingsSerializer(data=rules)
        self.assertEquals(False, serializer.is_valid())
        self.assertEquals("Invalid parameter value: ['es', 'es']",
                          serializer.errors['binding_rules'][0]['group_rules'][0]['value'][0],
                          'Invalid error message')

    def test_deserialize_binding_Invalid_origin_should_give_error(self):
        # We need to do import here in order generic patches work
        rules = {
                  'class_name': 'cli',
                  'origin': 'test.test',
                  'binding_rules':
                  [
                     {
                       "bindings": ["51c577679078b9023b3a2c4b"],
                       "group_rules": [{'operation': 'eq', 'input_context_param': 'ob', 'value': ['es']},
                                       {'operation': 'range', 'input_context_param': 'uuid', 'value': [1, 20]}]
                      }
                  ]
                }
        serializer = BindingsSerializer(data=rules)
        self.assertEquals(False, serializer.is_valid(), "Deserialization invalid")
        self.assertEquals("invalid",
                          serializer.errors['origin'][0], 'Invalid error message')
        # We need to do import here in order generic patches work
        rules = {
                  'class_name': 'cli',
                  'origin': ' test',
                  'binding_rules':
                  [
                     {
                       "bindings": ["51c577679078b9023b3a2c4b"],
                       "group_rules": [{'operation': 'eq', 'input_context_param': 'ob', 'value': ['es']},
                                       {'operation': 'range', 'input_context_param': 'uuid', 'value': [1, 20]}]
                      }
                  ]
                }
        serializer = BindingsSerializer(data=rules)
        self.assertEquals(False, serializer.is_valid(), "Deserialization invalid")
        self.assertEquals("invalid",
                          serializer.errors['origin'][0], 'Invalid error message')

    def test_deserialize_binding_Invalid_class_name_should_give_error(self):
        # We need to do import here in order generic patches work
        rules = {
                  'class_name': 'cli.cli',
                  'origin': 'test',
                  'binding_rules':
                  [
                     {
                       "bindings": ["51c577679078b9023b3a2c4b"],
                       "group_rules": [{'operation': 'eq', 'input_context_param': 'ob', 'value': ['es']},
                                       {'operation': 'range', 'input_context_param': 'uuid', 'value': [1, 20]}]
                      }
                  ]
                }
        serializer = BindingsSerializer(data=rules)
        self.assertEquals(False, serializer.is_valid(), "Deserialization invalid")
        self.assertEquals("invalid",
                          serializer.errors['class_name'][0], 'Invalid error message')
        # We need to do import here in order generic patches work
        rules = {
                  'class_name': ' cli',
                  'origin': 'test',
                  'binding_rules':
                  [
                     {
                       "bindings": ["51c577679078b9023b3a2c4b"],
                       "group_rules": [{'operation': 'eq', 'input_context_param': 'ob', 'value': ['es']},
                                       {'operation': 'range', 'input_context_param': 'uuid', 'value': [1, 20]}]
                      }
                  ]
                }
        serializer = BindingsSerializer(data=rules)
        self.assertEquals(False, serializer.is_valid(), "Deserialization invalid")
        self.assertEquals("invalid",
                          serializer.errors['class_name'][0], 'Invalid error message')
