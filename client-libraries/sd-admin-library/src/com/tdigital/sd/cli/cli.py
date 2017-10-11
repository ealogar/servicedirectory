'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
from __future__ import print_function
from ConfigParser import ConfigParser, NoOptionError
from docopt import docopt
from io import StringIO
import json
from com.tdigital.sd.admin.client import Client
from com.tdigital.sd.admin.exceptions import SdAdminLibraryException, ServerException
from com.tdigital.sd.admin.classes import Classes
from com.tdigital.sd.admin.instances import Instances
from com.tdigital.sd.admin.info import Info
from com.tdigital.sd.admin.bindings import Bindings
from os.path import isfile, exists
from pkg_resources import Requirement, resource_filename, DistributionNotFound  # @UnresolvedImport
from sys import getfilesystemencoding


# POSIX format for the CLI arguments (input for docopt library to parse the command line)
CLI_DOC = """Service Directory CLI

Usage:
    sd-cli [-d] [-c conf] [-e url] [-u username] [-p password] [-n] [-k key] [-r cert] info
    sd-cli [-d] [-c conf] [-e url] [-u username] [-p password] [-n] [-k key] [-r cert] classes create <class_name> <default_version> [<description>]
    sd-cli [-d] [-c conf] [-e url] [-u username] [-p password] [-n] [-k key] [-r cert] classes find
    sd-cli [-d] [-c conf] [-e url] [-u username] [-p password] [-n] [-k key] [-r cert] classes get <class_name>
    sd-cli [-d] [-c conf] [-e url] [-u username] [-p password] [-n] [-k key] [-r cert] classes update <class_name> <params> ...
    sd-cli [-d] [-c conf] [-e url] [-u username] [-p password] [-n] [-k key] [-r cert] classes delete <class_name>
    sd-cli [-d] [-c conf] [-e url] [-u username] [-p password] [-n] [-k key] [-r cert] instances create <class_name> <version> <uri> <environment> [<attributes> ...]
    sd-cli [-d] [-c conf] [-e url] [-u username] [-p password] [-n] [-k key] [-r cert] instances find <class_name> [<params> ...]
    sd-cli [-d] [-c conf] [-e url] [-u username] [-p password] [-n] [-k key] [-r cert] instances get <class_name> <instance_id>
    sd-cli [-d] [-c conf] [-e url] [-u username] [-p password] [-n] [-k key] [-r cert] instances update <class_name> <instance_id> <params> ...
    sd-cli [-d] [-c conf] [-e url] [-u username] [-p password] [-n] [-k key] [-r cert] instances update-attrs <class_name> <instance_id> <attributes> ...
    sd-cli [-d] [-c conf] [-e url] [-u username] [-p password] [-n] [-k key] [-r cert] instances delete <class_name> <instance_id>
    sd-cli [-d] [-c conf] [-e url] [-u username] [-p password] [-n] [-k key] [-r cert] bindings create <class_name> <origin> <bindings.json>
    sd-cli [-d] [-c conf] [-e url] [-u username] [-p password] [-n] [-k key] [-r cert] bindings find [<params> ...]
    sd-cli [-d] [-c conf] [-e url] [-u username] [-p password] [-n] [-k key] [-r cert] bindings get <class_name> <origin>
    sd-cli [-d] [-c conf] [-e url] [-u username] [-p password] [-n] [-k key] [-r cert] bindings update <class_name> <origin> <bindings.json>
    sd-cli [-d] [-c conf] [-e url] [-u username] [-p password] [-n] [-k key] [-r cert] bindings delete <class_name> <origin>
    sd-cli (-h | --help)
    sd-cli (-v | --version)
    sd-cli (-s | --show-default-config)

Options:
    -d --debug                          Enable debugging.
    -c conf --conf=conf                 Path to the configuration file (with default url, username and password)
    -e --url=url                        Service directory URL (with the pattern <protocol>://<host>:<port>/sd/v1/)
    -u username --username=username     User name to access the service directory with basic authentication
    -p password --password=password     Password to access the service directory with basic authentication
    -n --noverify                       No verify server certificate
    -k --key=key                        Path to the client private key (.pem file) for 2-way SSL. It would also require --cert option
    -r --cert=cert                      Path to the client public certificate (.pem file) for 2-way SSL. It would also require --key option
    -h --help                           Show this screen.
    -v --version                        Show version.
    -dcp --default-config-path          Show default configuration file location
"""

# Version of the CLI (when using --version option)
CLI_VERSION = 'Service Directory CLI v1.0'

# Path to the default service directory configuration (we count on setuptools!)
try:
    DEFAULT_CONFIG_PATH = resource_filename(Requirement.parse("sd-admin-library"), "sd-config/cli.conf")
except DistributionNotFound:
    DEFAULT_CONFIG_PATH = None


def _show_default_config():
    print("Path to default config: {0}".format(DEFAULT_CONFIG_PATH))
    print("Content of file: ")
    try:
        with open(DEFAULT_CONFIG_PATH) as f:
            print(f.read())
    except IOError:
        print("Default config file not found. It must have been deleted.")


def _get_config(path):
    """Parse a configuration file

    Parse configuration file, available at path, to extract relevant information to connect
    to the remote service directory

    :param path Path to the configuration file
    return Dictionary with the configuration parameters parsed from the file
    """

    try:
        # Open the config file and prepare a pseudo section to make it parsable with ConfigParser
        f = open(path, "r")
        pseudo_config = StringIO(u'[SD]\n' + f.read())
        parser = ConfigParser()
        parser.readfp(pseudo_config)

        # Prepare a dictionary with the required config parameters
        config = dict()
        for param_key in ('url', 'username', 'password', 'timeout'):
            try:
                config[param_key] = parser.get('SD', param_key)
            except NoOptionError:
                raise SdAdminLibraryException('Configuration parameter \"' + param_key + '\" is required')

        # Required config can not be empty strings
        if any(map(lambda x: x.strip() == '', config.itervalues())):
            raise SdAdminLibraryException('url, username and password can not be empty')
        # timeout must be integer
        try:
            config['timeout'] = int(config['timeout'])
        except ValueError:
            raise SdAdminLibraryException('timeout must be intenger')

        # Add optional config parameters
        try:
            config['verify'] = parser.getboolean('SD', 'verify')
        except ValueError:
            raise SdAdminLibraryException('The configuration parameter \"verify\" must be boolean')
        except NoOptionError:
            pass
        try:
            config['key'] = parser.get('SD', 'key')
        except NoOptionError:
            pass
        try:
            config['cert'] = parser.get('SD', 'cert')
        except NoOptionError:
            pass

        return config
    except IOError:
        raise SdAdminLibraryException('Error reading file \"' + path + '\"')


def _get_client(arguments):
    """Get the HTTP client to the service directory

    Retrieve the default configuration for the service directory CLI and override with the command line
    options

    :param arguments CLI arguments formatted with docopt
    :return Client object to access the service directory
    """

    # Check if the user wants to override the configuration file
    config_path = arguments.get('--conf')
    if config_path == None:
        # Get the path to the default configuration
        config_path = DEFAULT_CONFIG_PATH
    # Parse the configuration file
    client_config = _get_config(config_path)

    # Override the default configuration with the options (if any) set in the command line
    for config_key in client_config.iterkeys():
        option = '--' + config_key
        if arguments.get(option) is not None:
            client_config[config_key] = arguments.get(option)

    # Check noverify option (it is not covered by the previous loop because it is set to "verify" parameter)
    if arguments.get('--noverify'):
        client_config['verify'] = False

    # Prepare tuple for client certificate (cert and key) if 2-way ssl required
    try:
        cert = client_config['cert']
        key = client_config['key']
        if not cert or not key:
            raise SdAdminLibraryException('To enable 2-way SSL, both certificate and private key must be set')
        # Verify that both files exist
        if not isfile(cert):
            raise SdAdminLibraryException('Invalid certificate path \"' + cert + '\"')
        if not isfile(key):
            raise SdAdminLibraryException('Invalid private key path \"' + key + '\"')
        # Save the certificate as a tuple (valid for "requests" library)
        del client_config['key']  # This param is not needed anymore
        client_config['cert'] = (cert, key)
    except KeyError:
        pass

    if arguments.get('--debug'):
        client_config['debug'] = True
        print('')
        print('[CLI Configuration]:')
        print(_format(client_config))

    return Client(**client_config)


def _format(dictionary):
    """Pretty format a dictionary

    Format a dictionary object into a well formatted JSON string

    :param dictionary Dictionary object to be pretty formatted
    :return String with a pretty format of a dictionary or JSON document
    """

    return json.dumps(dictionary, ensure_ascii=False, sort_keys=True, indent=2)


def _validate_non_empty(name, value):
    if value.strip() == '':
        raise SdAdminLibraryException('{0} argument can not be empty'.format(name))


def _validate_params(params, invalid_keys, allowed_keys=None):
    """Check params dictionary does not contain any invalid key

    Validate params dict by checking that no invalid key (from invalid_keys list) is included in params dict keys

    :param params Params dictionary
    :param invalid_keys List of keys not permitted in params dictionary
    :param allowed_keys
    """

    for key in invalid_keys:
        if key in params.keys():
            raise SdAdminLibraryException('\"{0}\" cannot be part of <params>'.format(key))

    if allowed_keys:
        invalid_keys = filter(lambda x: x not in allowed_keys, params)
        for key in params.keys():
            if key not in allowed_keys:
                raise SdAdminLibraryException('\"{0}\" cannot be part of <params>'.format(key))


def _parse_params(params, params_name='<params>'):
    """Parse <params> into a dictionary

    Convert <params> list into a dictionary. Each <params> list element has the format: key=value
    where both key, value, and the tuple may be surrounded by "" to include spaces. These "" are
    removed.

    Repeated keys are not allowed so if one is repeated, an error will be launched.

    :param params List of strings with the optional <params> of the CLI
    :return Dictionary with the params list formatted
    """
    params_dict = {}
    if params:
        # param should have the format: key=value. However, " might be used for the key, value, or the pair (in order
        # to support spaces)
        for param in params:
            # Only one split (2 list elements)
            tokens = param.split('=', 1)
            if len(tokens) != 2:
                raise SdAdminLibraryException('{0} should match the format <key>=<value>'.format(params_name))
            else:
                key_dict = tokens[0].strip('"')  # remove the first "
                if key_dict in params_dict:
                    raise SdAdminLibraryException('{0} <key> can not be repeated'.format(key_dict))
                params_dict[key_dict] = tokens[1].strip('"')
    return params_dict


def _parse_json_file(path):
    """Parse a JSON file into a dict

    Open JSON file, available at path, and parse its content into a dictionary. The file must exist, with JSON content,
    and read access by the cli user.

    :param path Path to the JSON file
    :return Dictionary after parsing the JSON content of the file
    """
    if not exists(path):
        raise SdAdminLibraryException('Not existing file {0}'.format(path))
    with open(path, "r") as f:
        try:
            json_content = json.loads(f.read())
            if not isinstance(json_content, dict):
                raise SdAdminLibraryException('Json file should be a valid object (not array or null)')
            return json_content
        except ValueError as e:
            raise SdAdminLibraryException('Error parsing JSON file: {0}'.format(str(e)))


def _command_info(client, arguments):
    """Handle the "info" command

    Handle the "info" command, from the CLI, to get information about the service directory

    :param client Client object to access the service directory
    :param arguments CLI arguments formatted with docopt
    """

    info = Info(client)
    doc = info.info()
    print(_format(doc))


def _command_classes(client, arguments):
    """Handle the "classes" commands

    Handle the "classes" commands, from the CLI, to administrate the CLASS in the service directory

    :param client Client object to access the service directory
    :param arguments CLI arguments formatted with docopt
    """

    classes = Classes(client)
    class_name = arguments.get('<class_name>')
    # Switch which subcommand is to be executed for classes
    if arguments.get('create'):
        doc = classes.create(
            class_name,
            arguments.get('<default_version>'),
            arguments.get('<description>'))
        print('Created class: {0}'.format(class_name))
    elif arguments.get('find'):
        doc = classes.find()
        if doc and len(doc) > 0:
            print(_format(doc))
        else:
            print('No class matching these filter criteria')
    elif arguments.get('get'):
        doc = classes.get(class_name)
        print(_format(doc))
    elif arguments.get('update'):
        params = _parse_params(arguments.get('<params>'))
        _validate_params(params, ['class_name'])
        classes.update(class_name, **params)
        print('Updated class: ' + class_name)
    elif arguments.get('delete'):
        classes.delete(class_name)
        print('Deleted class: ' + class_name)


def _command_instances(client, arguments):
    """Handle the "instances" commands

    Handle the "instances" commands, from the CLI, to administrate the instances in the service directory

    :param client Client object to access the service directory
    :param arguments CLI arguments formatted with docopt
    """

    instances = Instances(client)
    class_name = arguments.get('<class_name>')
    instance_id = arguments.get('<instance_id>')
    _validate_non_empty('<class_name>', class_name)

    if arguments.get('create'):
        attributes = _parse_params(arguments.get('<attributes>'), '<attributes>')
        doc = instances.create(
            class_name,
            arguments.get('<version>'),
            arguments.get('<environment>'),
            arguments.get('<uri>'),
            **attributes)
        print('Created instance: {0}'.format(doc['id']))
    elif arguments.get('find'):
        params = _parse_params(arguments.get('<params>'))
        # Although is allowed, class_name should be only used in path param
        _validate_params(params, ['class_name'])
        doc = instances.find(class_name, **params)
        if doc:
            print(_format(doc))
        else:
            print('No instance matching these filter criteria')
    elif arguments.get('get'):
        _validate_non_empty('<instance_id>', instance_id)
        doc = instances.get(class_name, instance_id)
        print(_format(doc))
    elif arguments.get('update'):
        params = _parse_params(arguments.get('<params>'))
        _validate_non_empty('<instance_id>', instance_id)
        _validate_params(params, ('class_name', 'instance_id'), ('url', 'version', 'environment'))
        instances.update(class_name, instance_id, params=params)
        print('Updated instance: ' + instance_id)
    elif arguments.get('update-attrs'):
        attributes = _parse_params(arguments.get('<attributes>'))
        _validate_non_empty('<instance_id>', instance_id)
        instances.update(class_name, instance_id, attributes=attributes)
        print('Updated instance attributes: ' + instance_id)
    elif arguments.get('delete'):
        _validate_non_empty('<instance_id>', instance_id)
        instances.delete(class_name, instance_id)
        print('Deleted instance: {0} in class: {1}'.format(instance_id, class_name))


def _command_bindings(client, arguments):
    """Handle the "bindings" commands

    Handle the "bindings" commands, from the CLI, to administrate the client bindings in the service directory

    :param client Client object to access the service directory
    :param arguments CLI arguments formatted with docopt
    """
    bindings = Bindings(client)
    class_name = arguments.get('<class_name>')
    origin = arguments.get('<origin>')
    if arguments.get('create'):
        # Get the bindings json file content
        client_bindings = _parse_json_file(arguments.get('<bindings.json>'))
        bindings.create(class_name, origin, client_bindings)
        print('Created binding for class: {0} and origin: {1}'.format(class_name, origin))
    elif arguments.get('find'):
        params = _parse_params(arguments.get('<params>'))
        _validate_params(params, (), ('class_name', 'origin'))
        doc = bindings.find(**params)
        if doc and len(doc) > 0:
            print(_format(doc))
        else:
            print('No bindings matching these filter criteria')
    elif arguments.get('get'):
        doc = bindings.get(class_name, origin)
        print(_format(doc))
    elif arguments.get('update'):
        client_bindings = _parse_json_file(arguments.get('<bindings.json>'))
        bindings.update(class_name, origin, client_bindings)
        print('Updated binding for class: {0} and origin: {1}'.format(class_name, origin))
    elif arguments.get('delete'):
        bindings.delete(class_name, origin)
        print('Deleted bindings for class: {class_name} and origin: {origin}'.format(origin=origin,
                                                                                    class_name=class_name))


def convert_to_unicode_dict(input_dict):
    unicode_dict = dict()
    for key, value in input_dict.iteritems():
        key_unicode = unicode(key, getfilesystemencoding())
        if isinstance(value, list):  # not generic, just whit our expected dict
            value_unicode = map(lambda x: unicode(x, getfilesystemencoding()) \
                                if isinstance(x, basestring) else x, value)
        elif isinstance(value, basestring):
            value_unicode = unicode(value, getfilesystemencoding())
        else:
            value_unicode = value
        unicode_dict[key_unicode] = value_unicode
    return unicode_dict


def command():
    """Parse the CLI arguments and execute the command

    Parse the CLI arguments, with docopt, according to CLI specification in CLI_DOC
    and execute the required command.
    The library docopt will validate the syntax of the CLI command
    """

    # Parse and validate the command line, converting to unicode
    #command_line = map(lambda x: x.decode(sys.getfilesystemencoding()), sys.argv[1:])
    # Convert arguments to unicode
    arguments = convert_to_unicode_dict(docopt(CLI_DOC, version=CLI_VERSION))

    if arguments.get('-s') or arguments.get('--show-default-config'):
        _show_default_config()
    else:
        try:
            client = _get_client(arguments)
            # Target each command to a specific method
            if arguments.get('info'):
                _command_info(client, arguments)
            elif arguments.get('classes'):
                _command_classes(client, arguments)
            elif arguments.get('instances'):
                _command_instances(client, arguments)
            elif arguments.get('bindings'):
                _command_bindings(client, arguments)
        except ServerException as e:
            print('[SD Error]:')
            print(u'code: {0}'.format(e.json_details['exceptionId']))
            print(u'message: {0}'.format(e.json_details['exceptionText']))
        except SdAdminLibraryException as e:
            print('[CLI Error]:')
            print(str(e))
        except Exception as e:
            print('[CLI Error]:')
            msg = 'It seems that something goes wrong. Contact the operator for further assistance.'
            if arguments.get('--debug'):
                print('Error details: {0}'.format(str(e)))
            print(msg)


if __name__ == "__main__":
    command()
