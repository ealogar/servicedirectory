'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
from contextlib import nested

from httpretty import register_uri, GET, PUT, POST, DELETE, activate  # @UnresolvedImport
import json
import sys
import unittest
from mock import patch, mock_open, ANY, call
from com.tdigital.sd.cli import cli
from com.tdigital.sd.admin.exceptions import SdAdminLibraryException


class TestCli(unittest.TestCase):

    RESPONSE_API_CREATED = {
        'class_name': 'fake',
        'default_version': 'v1.0',
        'description': 'fake test'
    }

    RESPONSE_INSTANCE_CREATED = {
      'id': 'fake_id',
      'class_name': 'fake',
      'version': 'v1.0',
      'url': 'http://fake',
      'environment': 'dev',
      'attributes': {
          'protocol': 'https',
          'custom': 'fake'
        }
    }

    RULES = {
        'group_rules': [],
        'bindings': ['fake']

    }

    RESPONSE_BINDING_CREATED = {
      'id': 'fake_id',
      'class_name': 'fake',
      'origin': 'fakeorigin',
      'binding_rules': RULES,

    }

    RESPONSE_NOT_FOUND = {
        'exceptionId': 'SVC',
        'exceptionText': 'The resource xxx was not found'
    }

    CONFIG_FILE = '''
# example conf file
url=http://localhost:8000/sd/v1/
username=admin
password=admin
timeout=10
verify=true
cert=cert.fake
key=key.fake
'''

    def setUp(self):
        self.base_url = 'http://sd_fake.com/sd/v1/'

    @activate
    def test_info(self):
        register_uri(
            GET,
            'http://sd_fake.com/sd/info',
            body=json.dumps({'version': '1.0'}),
            status=200,
            content_type='application/json')
        sys.argv = ['sd-cli', 'info', '-d']
        with nested(patch('com.tdigital.sd.cli.cli._get_config'),
                    patch('com.tdigital.sd.cli.cli._format')) as(get_config_mock, format_mock):
            # import doing here to use patch
            config_dict = {'url': self.base_url, 'username': 'test', 'password': 'test'}
            get_config_mock.return_value = config_dict
            format_mock.return_value = 'Format Mock'
            cli.command()
            format_mock.assert_has_calls([call(config_dict), call({'version': '1.0'})])

    @activate
    def test_get_api(self):
        register_uri(
            GET,
            self.base_url + 'classes/fake',
            body=json.dumps(TestCli.RESPONSE_API_CREATED),
            status=200,
            content_type='application/json')
        sys.argv = ['sd-cli', 'classes', 'get', 'fake']
        with nested(patch('com.tdigital.sd.cli.cli._get_config'),
                    patch('com.tdigital.sd.cli.cli._format')) as(get_config_mock, format_mock):
            # import doing here to use patch
            get_config_mock.return_value = {'url': self.base_url, 'username': 'test',
                                            'password': 'test'}
            format_mock.return_value = 'Format Mock'
            cli.command()
            format_mock.assert_called_once_with(self.RESPONSE_API_CREATED)

    @activate
    def test_delete_api(self):
        register_uri(
            DELETE,
            self.base_url + 'classes/fake',
            body=None,
            status=204,
            content_type='application/json')
        sys.argv = ['sd-cli', 'classes', 'delete', 'fake']
        with nested(patch('com.tdigital.sd.cli.cli._get_config'),
                    patch('com.tdigital.sd.cli.cli._format')) as(get_config_mock, format_mock):
            # import doing here to use patch
            get_config_mock.return_value = {'url': self.base_url, 'username': 'test',
                                            'password': 'test'}
            format_mock.return_value = 'Format Mock'
            cli.command()
            self.assertEquals(0, format_mock.call_count)

    @activate
    def test_new_api(self):
        register_uri(
            POST,
            self.base_url + 'classes',
            body=json.dumps(TestCli.RESPONSE_API_CREATED),
            status=201,
            content_type='application/json')
        sys.argv = ['sd-cli', 'classes', 'create', 'fake', 'v1.0', 'fake test']
        with nested(patch('com.tdigital.sd.cli.cli._get_config'),
                    patch('com.tdigital.sd.cli.cli._format')) as(get_config_mock, format_mock):
            # import doing here to use patch
            get_config_mock.return_value = {'url': self.base_url, 'username': 'test',
                                            'password': 'test'}
            format_mock.return_value = 'Format Mock'
            cli.command()
            self.assertEquals(0, format_mock.call_count)
            # format_mock.assert_called_once_with(self.RESPONSE_API_CREATED)

    @activate
    def test_update_api(self):
        register_uri(
            POST,
            self.base_url + 'classes/fake',
            body=json.dumps(TestCli.RESPONSE_API_CREATED),
            status=200,
            content_type='application/json')
        register_uri(
            GET,
            self.base_url + 'classes/fake',
            body=json.dumps(TestCli.RESPONSE_API_CREATED),
            status=200,
            content_type='application/json')
        sys.argv = ['sd-cli', 'classes', 'update', 'fake', 'default_version=v1.0']
        with nested(patch('com.tdigital.sd.cli.cli._get_config'),
                    patch('com.tdigital.sd.cli.cli._format')) as(get_config_mock, format_mock):
            # import doing here to use patch
            get_config_mock.return_value = {'url': self.base_url, 'username': 'test',
                                            'password': 'test'}
            format_mock.return_value = 'Format Mock'
            cli.command()
            self.assertEquals(0, format_mock.call_count)
            # format_mock.assert_called_once_with(self.RESPONSE_API_CREATED)

    @activate
    def test_get_nonexisting_api(self):
        register_uri(
            GET,
            self.base_url + 'classes/fake',
            body=json.dumps(TestCli.RESPONSE_NOT_FOUND),
            status=404,
            content_type='application/json')

        sys.argv = ['sd-cli', 'classes', 'get', 'fake']
        with nested(patch('com.tdigital.sd.cli.cli._get_config'),
                    patch('com.tdigital.sd.cli.cli._format')) as(get_config_mock, format_mock):
            # import doing here to use patch
            get_config_mock.return_value = {'url': self.base_url, 'username': 'test',
                                            'password': 'test'}
            format_mock.return_value = 'Format Mock'
            cli.command()
            self.assertEquals(0, format_mock.call_count)
            # format_mock.assert_called_once_with(TestCli.RESPONSE_NOT_FOUND)

    @activate
    def test_find_apis(self):
        register_uri(
            GET,
            self.base_url + 'classes',
            body=json.dumps(list(TestCli.RESPONSE_API_CREATED)),
            status=200,
            content_type='application/json')
        sys.argv = ['sd-cli', 'classes', 'find']
        with patch('com.tdigital.sd.cli.cli._get_config') as get_config_mock:
            # import doing here to use patch
            get_config_mock.return_value = {'url': self.base_url, 'username': 'test',
                                            'password': 'test'}
            cli.command()

    @activate
    def test_find_apis_no_result(self):
        register_uri(
            GET,
            self.base_url + 'classes',
            body=json.dumps([]),
            status=200,
            content_type='application/json')
        sys.argv = ['sd-cli', 'classes', 'find']
        with patch('com.tdigital.sd.cli.cli._get_config') as get_config_mock,\
            patch('__builtin__.print') as print_mock:
            # import doing here to use patch
            get_config_mock.return_value = {'url': self.base_url, 'username': 'test',
                                            'password': 'test'}
            cli.command()
            print_mock.assert_called_once_with('No class matching these filter criteria')

    @activate
    def test_new_instance(self):
        register_uri(
            POST,
            self.base_url + 'classes/fake/instances',
            body=json.dumps(TestCli.RESPONSE_INSTANCE_CREATED),
            content_type='application/json')
        sys.argv = ['sd-cli', 'instances', 'create', 'fake', 'v1.0', 'http://fake', 'dev',
                    'protocol=https', 'custom=fake']
        with nested(patch('com.tdigital.sd.cli.cli._get_config'),
                    patch('com.tdigital.sd.cli.cli._format')) as(get_config_mock, format_mock):
            # import doing here to use patch
            get_config_mock.return_value = {'url': self.base_url, 'username': 'test',
                                            'password': 'test'}
            format_mock.return_value = 'Format Mock'
            cli.command()
            self.assertEquals(0, format_mock.call_count)
            # format_mock.assert_called_once_with(self.RESPONSE_INSTANCE_CREATED)

    @activate
    def test_update_instance(self):
        register_uri(
            GET,
            self.base_url + 'classes/fake/instances/fake_id',
            body=json.dumps(TestCli.RESPONSE_INSTANCE_CREATED),
            content_type='application/json')
        register_uri(
            PUT,
            self.base_url + 'classes/fake/instances/fake_id',
            body=json.dumps(TestCli.RESPONSE_INSTANCE_CREATED),
            content_type='application/json')
        sys.argv = ['sd-cli', 'instances', 'update', 'fake', 'fake_id', 'version=v1.0']
        with patch('com.tdigital.sd.cli.cli._get_config') as get_config_mock,\
                    patch('com.tdigital.sd.cli.cli._format') as format_mock,\
                    patch('__builtin__.print') as print_mock:
            # import doing here to use patch
            get_config_mock.return_value = {'url': self.base_url, 'username': 'test',
                                            'password': 'test'}
            format_mock.return_value = 'Format Mock'
            cli.command()
            self.assertEquals(0, format_mock.call_count)
            print_mock.assert_called_once_with('Updated instance: fake_id')

    @activate
    def test_update_instance_attrs(self):
        register_uri(
            GET,
            self.base_url + 'classes/fake/instances/fake_id',
            body=json.dumps(TestCli.RESPONSE_INSTANCE_CREATED),
            content_type='application/json')
        instance_upd = self.RESPONSE_INSTANCE_CREATED.copy()
        instance_upd['attributes']['protocol'] = 'https'
        register_uri(
            PUT,
            self.base_url + 'classes/fake/instances/fake_id',
            body=json.dumps(TestCli.RESPONSE_INSTANCE_CREATED),
            content_type='application/json')
        sys.argv = ['sd-cli', 'instances', 'update-attrs', 'fake', 'fake_id', 'protocol=v1.0']
        with nested(patch('com.tdigital.sd.cli.cli._get_config'),
                    patch('com.tdigital.sd.cli.cli._format')) as(get_config_mock, format_mock):
            # import doing here to use patch
            get_config_mock.return_value = {'url': self.base_url, 'username': 'test',
                                            'password': 'test'}
            format_mock.return_value = 'Format Mock'
            cli.command()
            self.assertEquals(0, format_mock.call_count)
            # format_mock.assert_called_once_with(self.RESPONSE_INSTANCE_CREATED)

    @activate
    def test_find_instance(self):
        register_uri(
            GET,
            self.base_url + 'classes/fake/instances',
            body=json.dumps([TestCli.RESPONSE_INSTANCE_CREATED]),
            content_type='application/json')
        sys.argv = ['sd-cli', 'instances', 'find', 'fake']
        with nested(patch('com.tdigital.sd.cli.cli._get_config'),
                    patch('com.tdigital.sd.cli.cli._format')) as(get_config_mock, format_mock):
            # import doing here to use patch
            get_config_mock.return_value = {'url': self.base_url, 'username': 'test',
                                            'password': 'test'}
            format_mock.return_value = 'Format Mock'
            cli.command()
            format_mock.assert_called_once_with([self.RESPONSE_INSTANCE_CREATED])

    @activate
    def test_find_instance_no_results(self):
        register_uri(
            GET,
            self.base_url + 'classes/fake/instances',
            body=json.dumps([]),
            content_type='application/json')
        sys.argv = ['sd-cli', 'instances', 'find', 'fake']
        with patch('com.tdigital.sd.cli.cli._get_config') as get_config_mock,\
                    patch('com.tdigital.sd.cli.cli._format') as format_mock,\
                    patch('__builtin__.print') as print_mock:
            # import doing here to use patch
            get_config_mock.return_value = {'url': self.base_url, 'username': 'test',
                                            'password': 'test'}
            format_mock.return_value = 'Format Mock'
            cli.command()
            print_mock.assert_called_once_with('No instance matching these filter criteria')

    @activate
    def test_get_instance(self):
        register_uri(
            GET,
            self.base_url + 'classes/fake/instances/fake_instance_id',
            body=json.dumps(TestCli.RESPONSE_INSTANCE_CREATED),
            content_type='application/json')
        sys.argv = ['sd-cli', 'instances', 'get', 'fake', 'fake_instance_id']
        with nested(patch('com.tdigital.sd.cli.cli._get_config'),
                    patch('com.tdigital.sd.cli.cli._format')) as(get_config_mock, format_mock):
            # import doing here to use patch
            get_config_mock.return_value = {'url': self.base_url, 'username': 'test',
                                            'password': 'test'}
            format_mock.return_value = 'Format Mock'
            cli.command()
            format_mock.assert_called_once_with(self.RESPONSE_INSTANCE_CREATED)

    @activate
    def test_delete_instance(self):
        register_uri(
            DELETE,
            self.base_url + 'classes/fake/instances/fake_instance_id',
            body=None,
            status=204,
            content_type='application/json')
        sys.argv = ['sd-cli', 'instances', 'delete', 'fake', 'fake_instance_id']
        with nested(patch('com.tdigital.sd.cli.cli._get_config'),
                    patch('com.tdigital.sd.cli.cli._format')) as(get_config_mock, format_mock):
            # import doing here to use patch
            get_config_mock.return_value = {'url': self.base_url, 'username': 'test',
                                            'password': 'test'}
            format_mock.return_value = 'Format Mock'
            cli.command()
            self.assertEquals(0, format_mock.call_count)

    @activate
    def test_new_binding(self):
        register_uri(
            POST,
            self.base_url + 'bindings',
            body=json.dumps(TestCli.RESPONSE_BINDING_CREATED),
            content_type='application/json')
        sys.argv = ['sd-cli', 'bindings', 'create', 'fake', 'fakeorigin', 'fake.json']
        with nested(patch('com.tdigital.sd.cli.cli._get_config'),
                    patch('com.tdigital.sd.cli.cli._format'),
                    patch('__builtin__.open', mock_open(read_data=json.dumps(TestCli.RULES)), create=True),
                    patch('com.tdigital.sd.cli.cli.exists')) as(get_config_mock, format_mock, file_mock, exists_mock):
            # import doing here to use patch
            exists_mock.return_value = True
            get_config_mock.return_value = {'url': self.base_url, 'username': 'test',
                                            'password': 'test'}
            format_mock.return_value = 'Format Mock'
            cli.command()
            self.assertEquals(0, format_mock.call_count)
            # format_mock.assert_called_once_with(self.RESPONSE_BINDING_CREATED)
            file_mock.assert_called_once_with('fake.json', "r")

    @activate
    def test_new_binding_non_existing_json_file(self):
        register_uri(
            POST,
            self.base_url + 'bindings',
            body=json.dumps(TestCli.RESPONSE_BINDING_CREATED),
            content_type='application/json')
        sys.argv = ['sd-cli', 'bindings', 'create', 'fake', 'fakeorigin', 'fake-not-existing.json']
        with patch('com.tdigital.sd.cli.cli._get_config') as get_config_mock,\
                    patch('com.tdigital.sd.cli.cli._format') as format_mock,\
                    patch('com.tdigital.sd.cli.cli.exists') as exists_mock,\
                    patch('__builtin__.print') as print_mock:
            # import doing here to use patch
            exists_mock.return_value = False
            get_config_mock.return_value = {'url': self.base_url, 'username': 'test',
                                            'password': 'test'}
            format_mock.return_value = 'Format Mock'
            cli.command()
            self.assertEquals(0, format_mock.call_count)
            print_mock.assert_has_calls([call('[CLI Error]:'),
                    call('Not existing file fake-not-existing.json')])

    @activate
    def test_new_binding_invalid_json_file(self):
        register_uri(
            POST,
            self.base_url + 'bindings',
            body=json.dumps(TestCli.RESPONSE_BINDING_CREATED),
            content_type='application/json')
        sys.argv = ['sd-cli', 'bindings', 'create', 'fake', 'fakeorigin', 'fake-not-good.json']
        with patch('com.tdigital.sd.cli.cli._get_config') as get_config_mock,\
            patch('com.tdigital.sd.cli.cli._format') as format_mock,\
            patch('com.tdigital.sd.cli.cli.exists') as exists_mock,\
            patch('__builtin__.open', mock_open(read_data='{'), create=True) as file_mock,\
            patch('__builtin__.print') as print_mock:
            # import doing here to use patch
            exists_mock.return_value = True
            get_config_mock.return_value = {'url': self.base_url, 'username': 'test',
                                            'password': 'test'}
            format_mock.return_value = 'Format Mock'
            cli.command()
            file_mock.assert_called_once_with('fake-not-good.json', "r")
            self.assertEquals(0, format_mock.call_count)
            print_mock.assert_has_calls([call('[CLI Error]:'),
                    call('Error parsing JSON file: Expecting object: line 1 column 1 (char 0)')])

    @activate
    def test_new_binding_invalid_object_json_file(self):
        register_uri(
            POST,
            self.base_url + 'bindings',
            body=json.dumps(TestCli.RESPONSE_BINDING_CREATED),
            content_type='application/json')
        sys.argv = ['sd-cli', 'bindings', 'create', 'fake', 'fakeorigin', 'fake-not-good.json']
        with patch('com.tdigital.sd.cli.cli._get_config') as get_config_mock,\
            patch('com.tdigital.sd.cli.cli._format') as format_mock,\
            patch('com.tdigital.sd.cli.cli.exists') as exists_mock,\
            patch('__builtin__.open', mock_open(read_data='[{"origin": "origin"}]'), create=True) as file_mock,\
            patch('__builtin__.print') as print_mock:
            # import doing here to use patch
            exists_mock.return_value = True
            get_config_mock.return_value = {'url': self.base_url, 'username': 'test',
                                            'password': 'test'}
            format_mock.return_value = 'Format Mock'
            cli.command()
            file_mock.assert_called_once_with('fake-not-good.json', "r")
            self.assertEquals(0, format_mock.call_count)
            print_mock.assert_has_calls([call('[CLI Error]:'),
                    call('Json file should be a valid object (not array or null)')])

    @activate
    def test_update_binding(self):
        register_uri(
            GET,
            self.base_url + 'bindings',
            body=json.dumps([TestCli.RESPONSE_BINDING_CREATED]),
            content_type='application/json')
        register_uri(
            PUT,
            self.base_url + 'bindings/fake_id',
            body=json.dumps(TestCli.RESPONSE_BINDING_CREATED),
            content_type='application/json')
        sys.argv = ['sd-cli', 'bindings', 'update', 'fake', 'fakeorigin', 'fake.json']
        with nested(patch('com.tdigital.sd.cli.cli._get_config'),
                    patch('com.tdigital.sd.cli.cli._format'),
                   patch('__builtin__.open', mock_open(read_data=json.dumps(TestCli.RULES)), create=True),
                    patch('com.tdigital.sd.cli.cli.exists')) as(get_config_mock, format_mock, file_mock, exists_mock):
            # import doing here to use patch
            exists_mock.return_value = True
            get_config_mock.return_value = {'url': self.base_url, 'username': 'test',
                                            'password': 'test'}
            format_mock.return_value = 'Format Mock'
            cli.command()
            self.assertEquals(0, format_mock.call_count)
            # format_mock.assert_called_once_with(self.RESPONSE_BINDING_CREATED)
            file_mock.assert_called_once_with('fake.json', "r")

    @activate
    def test_update_binding_invalid_binding_should_print_generic_problem(self):
        register_uri(
            GET,
            self.base_url + 'bindings',
            body=json.dumps([{'origin': 'tugo'}]),
            content_type='application/json')
        register_uri(
            PUT,
            self.base_url + 'bindings/fake_id',
            body=json.dumps(TestCli.RESPONSE_BINDING_CREATED),
            content_type='application/json')
        sys.argv = ['sd-cli', 'bindings', 'update', 'fake', 'fakeorigin', 'fake.json', '--debug']
        with patch('com.tdigital.sd.cli.cli._get_config') as get_config_mock,\
            patch('com.tdigital.sd.cli.cli._format') as format_mock,\
            patch('__builtin__.open', mock_open(read_data=json.dumps(TestCli.RULES)), create=True) as file_mock,\
            patch('com.tdigital.sd.cli.cli.exists') as exists_mock,\
            patch('__builtin__.print') as print_mock:
            # import doing here to use patch
            exists_mock.return_value = True
            get_config_mock.return_value = {'url': self.base_url, 'username': 'test',
                                            'password': 'test'}
            format_mock.return_value = 'Format Mock'
            cli.command()
            file_mock.assert_called_once_with('fake.json', "r")
            self.assertTrue(print_mock.call_count >= 20)
            self.assertTrue(call('It seems that something goes wrong. Contact the operator for further assistance.') in
                            print_mock.mock_calls)

    @activate
    def test_update_nonexisting_binding(self):
        register_uri(
            GET,
            self.base_url + 'bindings',
            status=200,
            body=[],
            content_type='application/json')
        sys.argv = ['sd-cli', 'bindings', 'update', 'fake', 'fakeorigin', 'fake.json']
        with nested(patch('com.tdigital.sd.cli.cli._get_config'),
                    patch('com.tdigital.sd.cli.cli._format'),
                   patch('__builtin__.open', mock_open(read_data=json.dumps(TestCli.RULES)), create=True),
                    patch('com.tdigital.sd.cli.cli.exists')) as(get_config_mock, format_mock, file_mock, exists_mock):
            # import doing here to use patch
            exists_mock.return_value = True
            get_config_mock.return_value = {'url': self.base_url, 'username': 'test',
                                            'password': 'test'}
            format_mock.return_value = 'Format Mock'
            cli.command()
            self.assertEquals(0, format_mock.call_count)
            file_mock.assert_called_once_with('fake.json', "r")

    @activate
    def test_delete_binding(self):
        register_uri(
            GET,
            self.base_url + 'bindings',
            body=json.dumps([TestCli.RESPONSE_BINDING_CREATED]),
            content_type='application/json')
        register_uri(
            DELETE,
            self.base_url + 'bindings/fake_id',
            body=None,
            status=204,
            content_type='application/json')
        sys.argv = ['sd-cli', 'bindings', 'delete', 'fake', 'fakeorigin']
        with nested(patch('com.tdigital.sd.cli.cli._get_config'),
                    patch('com.tdigital.sd.cli.cli._format')) as(get_config_mock, format_mock):
            # import doing here to use patch
            get_config_mock.return_value = {'url': self.base_url, 'username': 'test',
                                            'password': 'test'}
            format_mock.return_value = 'Format Mock'
            cli.command()
            self.assertEquals(0, format_mock.call_count, 'Format should not be called')

    @activate
    def test_delete_nonexisting_binding(self):
        register_uri(
            GET,
            self.base_url + 'bindings',
            body=[],
            content_type='application/json')
        sys.argv = ['sd-cli', 'bindings', 'delete', 'fake', 'fakeorigin']
        with nested(patch('com.tdigital.sd.cli.cli._get_config'),
                    patch('com.tdigital.sd.cli.cli._format')) as(get_config_mock, format_mock):
            # import doing here to use patch
            get_config_mock.return_value = {'url': self.base_url, 'username': 'test',
                                            'password': 'test'}
            format_mock.return_value = 'Format Mock'
            cli.command()
            self.assertEquals(0, format_mock.call_count, 'Format should not be called')

    @activate
    def test_find_bindings(self):
        register_uri(
            GET,
            self.base_url + 'bindings',
            body=json.dumps([TestCli.RESPONSE_BINDING_CREATED]),
            content_type='application/json')
        sys.argv = ['sd-cli', 'bindings', 'find']
        with nested(patch('com.tdigital.sd.cli.cli._get_config'),
                    patch('com.tdigital.sd.cli.cli._format')) as(get_config_mock, format_mock):
            # import doing here to use patch
            get_config_mock.return_value = {'url': self.base_url, 'username': 'test',
                                            'password': 'test'}
            format_mock.return_value = 'Format Mock'
            cli.command()
            format_mock.assert_called_once_with([self.RESPONSE_BINDING_CREATED])

    @activate
    def test_find_bindings_empty_result(self):
        register_uri(
            GET,
            self.base_url + 'bindings',
            body=json.dumps([]),
            content_type='application/json')
        sys.argv = ['sd-cli', 'bindings', 'find']
        with patch('com.tdigital.sd.cli.cli._get_config') as get_config_mock,\
                    patch('com.tdigital.sd.cli.cli._format') as format_mock,\
                    patch('__builtin__.print') as print_mock:
            # import doing here to use patch
            get_config_mock.return_value = {'url': self.base_url, 'username': 'test',
                                            'password': 'test'}
            format_mock.return_value = 'Format Mock'
            cli.command()
            print_mock.assert_called_once_with('No bindings matching these filter criteria')

    @activate
    def test_get_binding_unexisting(self):
        register_uri(
            GET,
            self.base_url + 'bindings',
            body=json.dumps([]),
            content_type='application/json')
        sys.argv = ['sd-cli', 'bindings', 'get', 'fake_not', 'origin_not']
        with patch('com.tdigital.sd.cli.cli._get_config') as get_config_mock,\
                    patch('com.tdigital.sd.cli.cli._format') as format_mock,\
                    patch('__builtin__.print') as print_mock:
            # import doing here to use patch
            get_config_mock.return_value = {'url': self.base_url, 'username': 'test',
                                            'password': 'test'}
            format_mock.return_value = 'Format Mock'
            cli.command()
            self.assertEquals(0, format_mock.call_count)
            self.assertEquals(2, print_mock.call_count)

    @activate
    def test_get_binding(self):
        register_uri(
            GET,
            self.base_url + 'bindings',
            body=json.dumps([TestCli.RESPONSE_BINDING_CREATED]),
            content_type='application/json')
        sys.argv = ['sd-cli', 'bindings', 'get', 'fake', 'fakeorigin']
        with nested(patch('com.tdigital.sd.cli.cli._get_config'),
                    patch('com.tdigital.sd.cli.cli._format')) as(get_config_mock, format_mock):
            # import doing here to use patch
            get_config_mock.return_value = {'url': self.base_url, 'username': 'test',
                                            'password': 'test'}
            format_mock.return_value = 'Format Mock'
            cli.command()
            format_mock.assert_called_once_with(self.RESPONSE_BINDING_CREATED)

    @activate
    def test_get_binding_with_config_ssl(self):
        register_uri(
            GET,
            self.base_url + 'bindings',
            body=json.dumps([TestCli.RESPONSE_BINDING_CREATED]),
            content_type='application/json')
        sys.argv = ['sd-cli', 'bindings', 'get', 'fake', 'fakeorigin']
        with nested(patch('com.tdigital.sd.cli.cli._get_config'),
                    patch('com.tdigital.sd.cli.cli._format'),
                    patch('com.tdigital.sd.cli.cli.isfile')) as(get_config_mock, format_mock, is_file_mock):
            # import doing here to use patch
            is_file_mock.return_value = True
            get_config_mock.return_value = {'url': self.base_url, 'username': 'test',
                                            'password': 'test', 'key': 'key', 'cert': 'cert'}
            format_mock.return_value = 'Format Mock'
            cli.command()
            format_mock.assert_called_once_with(self.RESPONSE_BINDING_CREATED)

    def test_parse_config_file(self):

        with nested(patch('__builtin__.open', mock_open(read_data=self.CONFIG_FILE), create=True),
                    patch('com.tdigital.sd.cli.cli.exists')) as(file_mock, exist_mock):
            exist_mock.return_value = True
            cli._get_config('fake.conf')
            file_mock.assert_called_once_with('fake.conf', "r")

    def test_parse_config_file_without_timeout(self):
        modify_config = '''
# example conf file
url=http://localhost:8000/sd/v1/
username=admin
password=admin
        '''
        with nested(patch('__builtin__.open', mock_open(read_data=modify_config), create=True),
                    patch('com.tdigital.sd.cli.cli.exists')) as(file_mock, exist_mock):
            exist_mock.return_value = True
            self.assertRaises(SdAdminLibraryException, cli._get_config, 'fake.conf')
            file_mock.assert_called_once_with('fake.conf', "r")

    def test_parse_config_file_without_ssl(self):
        modify_config = '''
# example conf file
url=http://localhost:8000/sd/v1/
username=admin
password=admin
timeout=10
        '''
        with nested(patch('__builtin__.open', mock_open(read_data=modify_config), create=True),
                    patch('com.tdigital.sd.cli.cli.exists')) as(file_mock, exist_mock):
            exist_mock.return_value = True
            cli._get_config('fake.conf')
            file_mock.assert_called_once_with('fake.conf', "r")

    def test_show_default_config(self):
        sys.argv = ['sd-cli', '-s']
        with patch('__builtin__.open', mock_open(read_data=json.dumps(TestCli.RULES)), create=True) as file_mock:
            cli.command()
            file_mock.assert_called_once_with(ANY)
        sys.argv = ['sd-cli', '--show-default-config']
        with patch('__builtin__.open', mock_open(read_data=json.dumps(TestCli.RULES)), create=True) as file_mock:
            cli.command()
            file_mock.assert_called_once_with(ANY)

if __name__ == "__main__":
    unittest.main()
