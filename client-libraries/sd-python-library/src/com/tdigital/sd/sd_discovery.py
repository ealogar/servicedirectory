'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
from requests import get, codes
from ConfigParser import ConfigParser, NoOptionError
import os
import sys
from io import StringIO
from com.tdigital.sd.exceptions import SDLibraryException, RemoteException,\
    ConnectionException
from requests.auth import HTTPBasicAuth
from requests.exceptions import Timeout, ConnectionError, TooManyRedirects
from functools import partial
import logging
from com.tdigital.sd.cache import lru_cache
from collections import namedtuple
from copy import deepcopy

logger = logging.getLogger(__name__)

_cache_size = 2000

_BindingInstance = namedtuple('BindingInstance', ['class_name', 'version', 'uri', 'environment', 'attributes'])


class ServiceDirectory(object):

    config_file = 'service-directory.properties'

    URL_GET_VERSION = 'http://{host}:{port}/sd/version'
    URL_SEARCH_ENDPOINTS = 'http://{host}:{port}/sd/{version}/bind_instances'
    SD_USER = 'admin'
    SD_PASSWORD = 'admin'

    def __init__(self, host=None, port=None, version=None,  ttl=None, ttr=None, timeout=None):
        """
        ServiceDirectory class provides an easy way of accessing the service directory to bind
        instances for a given class.

        It implements a cache internally to store the responses for a quick access.

        You can define the following parameters to control how it works:

        :param host The name of the service directory host (Mandatory)
        :param port The port of the service directory (Mandatory)
        :param version The service directory version, if no version is provided,
                       the last version of SD wil be used.

        :param ttl The Time to live of the cache. By default a value of 1 week will be used.
                   It must be expressed in hours. When expired, the response of the service
                   directory will be returned directly. This may happend only when Service
                   directory instances are not working for a long time.

        :param ttr The Time ro refresh of the cache. When expired, a new value from the service
                   directory will be taken to replace the existing one, updating ttl and ttr. It's
                   expressed in seconds and must be less than ttl.

        :param timeout The maximun time that a connection to the service directory will be waiting
                       for a response.

        Alternatively you can supply a config_file (any where in pythonpath with name service-directory.properties)
        with the upper variables that you want to supply. The values that you supply in config_file will be taken
        prior to the ones in __init__.

        >>from com.tdigital.sd.sd_discovery import ServiceDirectory
        >>library = ServiceDirectory('localhost', 80, 'v1', ttl=55, ttr=360, timeout=30)
        >>instance = library.bind_instance('sms', {'origin': 'tugo', 'environment': 'production', 'ob': 'uk'})
        >>print instance.class_name, instance.url, instance.attributes

        """

        # Check if config file provided inside python path
        config_file_path = None
        for dir_path in sys.path:
            if os.path.isdir(dir_path):
                if os.path.exists(os.path.join(dir_path, self.config_file)):
                    config_file_path = dir_path
                    break

        # If Config File is provided, we initialize
        if config_file_path:
            # override input parameters of constructor with properties set
            config = ConfigParser()
            # Make a pseudo section to use ConfigParser from python library
            pseudo_config = StringIO(''.join([u'[SD]\n',
                                    open(os.path.join(config_file_path, self.config_file)).read()]))
            config.readfp(pseudo_config)
            # We call this helper function to assign first constructor parameter if not None
            # after we will assing the config value; when anything is provided we will assing a default
            self._assign_with_priority('host', host, config, None)
            self._assign_with_priority('port', port, config, None)
            self._assign_with_priority('version', version, config, None)
            self._assign_with_priority('ttl', ttl, config, 168)
            self._assign_with_priority('ttr', ttr, config, 3600)
            self._assign_with_priority('timeout', timeout, config, 30)

        else:
            self.host = host
            self.port = port
            self.version = version
            # if we do selt.ttl = ttl or 3600, a value of zero would be considered as None
            self.ttl = 168 if ttl is None else ttl
            self.ttr = 3600 if ttr is None else ttr
            self.timeout = 30 if timeout is None else timeout

        # host and port must be provided
        if not self.host or not self.port:
            raise SDLibraryException("Initialization error: Host and port must be provided")

        # Convert values to int/string when required and check values are valid for initialize library
        self._sanitize()

        if not self.version:
            # recover version from sd
            url_get_version = self.URL_GET_VERSION.format(host=self.host, port=self.port)
            try:
                resp = get(url_get_version, timeout=self.timeout,
                                    auth=HTTPBasicAuth(self.SD_USER, self.SD_PASSWORD))
                if resp.status_code != codes.ok:  # @UndefinedVariable
                    raise SDLibraryException("Initialization error: Default Service Directory version can not be get")
                resp = resp.json()
                self.version = resp['default_version']
            except Timeout:
                raise SDLibraryException("Initialization error: Default Service Directory version can not be get")
            except KeyError:
                raise RemoteException("Default version not returned from sd")

        # partial evaluation of format to only call with class_name parameter each time
        self.url_search = self.URL_SEARCH_ENDPOINTS.format(host=self.host, port=self.port,
                                                            version=self.version)

        # We apply decorator here to dynamically set ttr and ttl in decorator
        # A zero value in ttl will disable caching
        if self.ttl != 0:
            self.bind_instance = lru_cache(maxsize=_cache_size, typed=True, ttr=self.ttr, ttl=self.ttl,
                                       exceptions=(RemoteException, ConnectionException))(self.bind_instance)

    def _assign_with_priority(self, attr, value, config, default_value):

        if value is None:
            try:
                setattr(self, attr, config.get('SD', attr))
            except NoOptionError:
                # Default value (Null parameter and no config file)
                setattr(self, attr, default_value)
        else:
            # value has preference when is not null (constructo initialize)
            setattr(self, attr, value)

    def _sanitize(self):
        """
        Force integer values to be stored as integer and floats as floats
        We like duck typing but we must inform our library users of errors
        """

        try:
            map(lambda param: setattr(self, param, int(getattr(self, param))), ('port', 'timeout'))
        except (ValueError, TypeError) as e:
            logger.error("".join(["Error sanitizing input values : ", str(e)]))
            raise SDLibraryException('Initialization error: port and timeout must be integer')
        try:
            map(lambda param: setattr(self, param, float(getattr(self, param))), ('ttl', 'ttr'))
        except (ValueError, TypeError) as e:
            logger.error("".join(["Error sanitizing input values : ", str(e)]))
            raise SDLibraryException('Initialization error: ttl and ttr must be float numbers')

        if self.ttl != 0:
            if self.ttl < (1.0 / 3600):
                raise SDLibraryException("Initialization error: ttl must be zero or greater than 1/3600 hours")
            if self.ttr > (self.ttl * 3600):
                raise SDLibraryException("Initialization error: ttr value (expressed in seconds) should be \
                                        less than ttl (given in hours)")
        else:
            logger.info("Cache system is disabled")

        if self.timeout < 1:
            raise SDLibraryException("Initialization error: timeout must be greater than 1 second")

    def bind_instance(self, class_name, context=None):
        """
        Try to recover a ServiceInstance for the given class_name that best suits the
        context given.
        SD will apply rules defined for the search.
        :param class_name
        :param context extra search parameters that you can provide for the search

        :return BindingInstance object
                BindingInstance is a class for easy access of the variables:
                    class_name, version, url, environment, attributes
                        attributes will be a dict with extra attributes of the binding instance
                    you can do BindingInstance.class_name or BindingInstance.url
        """
        try:
            if not context:
                query_parameters = {'class_name': class_name}
            else:
                # Some validations in input parameters
                if not isinstance(context, dict):
                    raise SDLibraryException("context should be a dict")
                query_parameters = deepcopy(context)
                query_parameters['class_name'] = class_name

            # Prepare query_parameters for search
            logger.info("Requesting instances from SD for class %s with context %s", class_name, context)
            resp = get(self.url_search, timeout=self.timeout,
                                auth=HTTPBasicAuth(self.SD_USER, self.SD_PASSWORD), params=query_parameters)

            # If response code is not 200, return SD description error
            resp_body = resp.json()  # SD responses are always in json
            if resp.status_code != codes.ok:  # @UndefinedVariable
                raise RemoteException(resp_body['exceptionText'])

            return _BindingInstance(class_name=resp_body['class_name'],
                                           version=resp_body['version'],
                                           uri=resp_body['uri'],
                                           environment=resp_body['environment'],
                                           attributes=resp_body['attributes'])
        except Timeout as e:
            logger.warning("Timeout when calling SD: %s", str(e))
            raise ConnectionException('No response from SD while getting instances')
        except (ConnectionError, TooManyRedirects) as es:
            logger.warning("Connection error returned from SD: %s", str(es))
            raise ConnectionException('Connection error with SD while getting instances')
        except RemoteException as e:
            logger.warning("Error in SD call: %s", str(e))
            raise e
        except (ValueError, KeyError):
            raise RemoteException('Bad response from SD while getting instances')
