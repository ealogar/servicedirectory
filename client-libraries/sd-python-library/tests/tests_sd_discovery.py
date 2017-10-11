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
from com.tdigital.sd.sd_discovery import ServiceDirectory
from mock import MagicMock, patch, ANY, call
import sys
import os
import time
from requests.exceptions import Timeout, TooManyRedirects
from com.tdigital.sd.exceptions import SDLibraryException, RemoteException,\
    ConnectionException


class TestSdDiscovery(unittest.TestCase):

    def setUp(self):
        self.patcher_request_get = patch('com.tdigital.sd.sd_discovery.get')
        self.requestGetMock = self.patcher_request_get.start()
        self.sdRespMock = MagicMock(name='sdRespMock')
        self.sdRespMock.status_code = 200

        # We dont care about rules in SD, just we want to unit test library
        self.sdRespMock.json.return_value = {
          "class_name": "test_api",
          "uri": "uri_test",
          "version": "1.0",
          "environment": "production",
          "attributes": {"ob": "oba"}
        }

        self.requestGetMock.return_value = self.sdRespMock

    def tearDown(self):
        self.sdRespMock.reset_mock()
        self.sdRespMock.json.reset_mock()
        self.sdRespMock.json.side_effect = None
        self.patcher_request_get.stop()

    def test_get_endpoints_uncached_should_return_existing(self):
        library = ServiceDirectory('localhost', 8000, 'v1')
        instance = library.bind_instance('test_api')
        self.assertEquals('test_api', instance.class_name)
        self.assertEquals('uri_test', instance.uri)
        self.assertEquals({"ob": "oba"}, instance.attributes)
        self.requestGetMock.assert_called_once_with(ANY, timeout=30, auth=ANY, params=ANY)

    def test_get_instance_cached_should_return_from_cache(self):
        library = ServiceDirectory('localhost', 8000, 'v1')
        instance = library.bind_instance('test_api')
        self.assertEquals('test_api', instance.class_name)
        self.assertEquals('uri_test', instance.uri)
        self.assertEquals({"ob": "oba"}, instance.attributes)

        # If we call get_endPoinst we must have the value cached
        instance = library.bind_instance('test_api')
        self.assertEquals('test_api', instance.class_name)
        self.assertEquals('uri_test', instance.uri)
        self.assertEquals({"ob": "oba"}, instance.attributes)
        self.requestGetMock.assert_called_once_with(ANY, timeout=30, auth=ANY, params=ANY)
        # Now we check the number of times cache is called
        info_cache = library.bind_instance.cache_info()
        self.assertEquals(1, info_cache.hits)

    @patch('com.tdigital.sd.sd_discovery._cache_size', 1)
    def test_get_endpoints_max_size_cached_reached_should_return_lru_from_cache(self):
        library = ServiceDirectory('localhost', 8000, 'v1')
        library.bind_instance('test_api')
        info_cache = library.bind_instance.cache_info()
        self.assertEquals(0, info_cache.hits)
        self.assertEquals(1, info_cache.currsize)
        self.assertEquals(1, info_cache.misses)

        # If we call get_endPoinst we must have the value cached
        library.bind_instance('test_api')
        info_cache = library.bind_instance.cache_info()
        self.assertEquals(1, info_cache.hits)
        self.assertEquals(1, info_cache.currsize)
        # We call sd and test_new_api must update cache but not hit
        library.bind_instance('test_new_api')
        info_cache = library.bind_instance.cache_info()
        self.assertEquals(1, info_cache.hits)
        self.assertEquals(1, info_cache.currsize)
        self.assertEquals(2, info_cache.misses)

        library.bind_instance('test_new_api')
        info_cache = library.bind_instance.cache_info()
        self.assertEquals(2, info_cache.hits)
        self.assertEquals(1, info_cache.currsize)  # as expected the cache maximun is reached
        self.assertEquals(2, info_cache.misses)

        # Only two calls to SD
        self.assertEquals(2, self.requestGetMock.call_count, "SD not called 2 times")
        self.requestGetMock.assert_has_calls([call(ANY, timeout=30, auth=ANY, params=ANY),
                                             call(ANY, timeout=30, auth=ANY, params=ANY)])
        library.bind_instance.cache_clear()
        info_cache = library.bind_instance.cache_info()
        self.assertEquals(0, info_cache.hits)
        self.assertEquals(0, info_cache.currsize)  # as expected the cache maximun is reached
        self.assertEquals(0, info_cache.misses)

    def test_init_library_with_config_file_should_get_values_from_config(self):
        path_properties = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config')
        sys.path.append(path_properties)
        library = ServiceDirectory()
        sys.path.remove(path_properties)
        self.assertEquals('localhosttest', library.host, "Host was not read from config file")
        self.assertEquals(9000, library.port, "Port was not read from config file")
        self.assertEquals(1, library.ttl, "ttl was not read from config file")
        self.assertEquals(60, library.ttr, "ttr was not read from config file")
        self.assertEquals(10, library.timeout, "timeout was not read from config file")
        self.assertEquals('v2', library.version, "timeout was not read from config file")

    def test_init_library_with_config_file_and_constructor_should_get_values_from_const_first(self):
        path_properties = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config')
        sys.path.append(path_properties)
        library = ServiceDirectory('hostconstructor', 9900, timeout=38)
        sys.path.remove(path_properties)
        self.assertEquals('hostconstructor', library.host, "Host was not read from init")
        self.assertEquals(9900, library.port, "Port was not read from omot")
        self.assertEquals(1, library.ttl, "ttl was not read from config file")
        self.assertEquals(60, library.ttr, "ttr was not read from config file")
        self.assertEquals(38, library.timeout, "timeout was not read from config file")
        self.assertEquals('v2', library.version, "timeout was not read from config file")

    def test_init_library_with_small_config_file_and_constructor_should_get_default_values(self):
        path_properties = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'small_config')
        sys.path.append(path_properties)
        library = ServiceDirectory('hostconstructor', 9900)
        sys.path.remove(path_properties)
        self.assertEquals('hostconstructor', library.host, "Host was not read from init")
        self.assertEquals(9900, library.port, "Port was not read from init")
        self.assertEquals(168, library.ttl, "ttl default incorrect")
        self.assertEquals(3600, library.ttr, "ttr default incorrect")
        self.assertEquals(30, library.timeout, "timeout default value incorrect")
        self.assertEquals('vsmall', library.version, "timeout was not read from config file")

    def test_init_library_with_wrong_values_should_raise_sd_library_exception(self):
        self.assertRaises(SDLibraryException, ServiceDirectory, "host")
        self.assertRaises(SDLibraryException, ServiceDirectory, "host", "port")
        self.assertRaises(SDLibraryException, ServiceDirectory, "host", 8000, 'v1', ttl='undefined')
        self.assertRaises(SDLibraryException, ServiceDirectory, "host", 8000, 'v1', ttl=90, ttr='bad')
        self.assertRaises(SDLibraryException, ServiceDirectory, "host", 8000, 'v1', ttl=90, ttr=90, timeout='bad')
        self.assertRaises(SDLibraryException, ServiceDirectory, "host", 8000, 'v1', ttl=1.0 / 3700, ttr=90, timeout=30)
        self.assertRaises(SDLibraryException, ServiceDirectory, "host", 8000, 'v1', ttl=1, ttr=4000, timeout=30)
        self.assertRaises(SDLibraryException, ServiceDirectory, "host", 8000, 'v1', ttl=16, ttr=3000, timeout=0.1)

    def test_init_library_without_version_should_get_last_version_from_sd(self):
        sdRespInfoMock = MagicMock(name='sdRespMockInfo')
        sdRespInfoMock.status_code = 200
        sdRespInfoMock.json.return_value = {"app_name": "Service Directory", "default_version": "vlast"}
        self.requestGetMock.return_value = sdRespInfoMock
        library = ServiceDirectory('localhost', 8000)
        self.assertEquals('localhost', library.host, "Host was not read from config file")
        self.assertEquals(8000, library.port, "Port was not read from config file")
        self.assertEquals(168, library.ttl, "ttl was not read from config file")
        self.assertEquals(3600, library.ttr, "ttr was not read from config file")
        self.assertEquals(30, library.timeout, "timeout was not read from config file")
        self.assertEquals('vlast', library.version, "version was not obtained from SD")

    def test_init_library_with_timeout_from_sd_should_raise_Remote_exception(self):
        sdRespInfoMock = MagicMock(name='sdRespMockInfo')
        sdRespInfoMock.status_code = 200
        sdRespInfoMock.json.return_value = {"app_name": "Service Directory", "wrong_version": "vlast"}
        self.requestGetMock.return_value = sdRespInfoMock
        self.assertRaises(RemoteException, ServiceDirectory, 'localhost', 8000)

    def test_init_library_with_error_from_sd_should_raise_Sd_exception(self):
        sdRespInfoMock = MagicMock(name='sdRespMockInfo')
        sdRespInfoMock.status_code = 500
        sdRespInfoMock.json.return_value = {"exceptionId": "SVC00000", "exceptionText": "vlast"}
        self.requestGetMock.return_value = sdRespInfoMock
        self.assertRaises(SDLibraryException, ServiceDirectory, 'localhost', 8000)

    def test_init_library_with_timeout_from_sd_should_raise_Sd_exception(self):
        self.requestGetMock.side_effect = Timeout()
        self.assertRaises(SDLibraryException, ServiceDirectory, 'localhost', 8000)

    def test_get_endpoints_ttl_zero_should_not_hit_cache(self):
        library = ServiceDirectory('localhost', 8000, 'v1', ttl=0, timeout=30)
        library.bind_instance('test_api')
        library.bind_instance('test_api')
        self.requestGetMock.assert_has_calls([call(ANY, timeout=30, auth=ANY, params=ANY),
                                              call(ANY, timeout=30, auth=ANY, params=ANY)])
        self.assertEquals(2, self.requestGetMock.call_count, "SD called more than 3 times")

    def test_get_endpoints_low_ttr_should_refresh_element(self):
        sdRespMock = MagicMock(name='sdRespMockRefresh')
        sdRespMock.status_code = 200
        sdRespMock.json.side_effect = [
        {"class_name": "test_api",
          "uri": "uri_test",
          "version": "1.0",
          "environment": "production",
          "attributes": {"ob": "oba"}}
        , {
          "class_name" : "test_api",
          "uri" : "uri_test_refreshed",
          "version" : "1.0",
          "environment" : "production",
          "attributes": {"ob": "oba"}
        }

        ]
        self.requestGetMock.return_value = sdRespMock
        library = ServiceDirectory('localhost', 8000, 'v1', ttl=1, ttr=1, timeout=30)
        instance = library.bind_instance('test_api')  # update cache and call SD
        self.assertEquals('uri_test', instance.uri)
        time.sleep(1.1)  # after 1 second the cache should be refreshed
        instance = library.bind_instance('test_api')  # refresh element cache and call SD
        self.assertEquals('uri_test_refreshed', instance.uri)
        self.requestGetMock.assert_has_calls([call(ANY, timeout=30, auth=ANY, params=ANY),
                                              call(ANY, timeout=30, auth=ANY, params=ANY)])
        self.assertEquals(2, self.requestGetMock.call_count, "SD called more than 3 times")

    def test_get_endpoints_ttr_expired_SD_Unavailable_should_return_cached(self):
        sdRespMock = MagicMock(name='sdRespMockRefresh')
        sdRespMock.status_code = 200
        returns = [
        {
          "class_name": "test_api",
          "uri": "uri_test",
          "version": "1.0",
          "environment": "production",
          "attributes": {"ob": "oba"}
        },
        Timeout('SD unavailable')
        ]

        def side_effect_calls(*args):
            result = returns.pop(0)
            if isinstance(result, Exception):
                raise result
            return result

        sdRespMock.json.side_effect = side_effect_calls
        self.requestGetMock.return_value = sdRespMock
        library = ServiceDirectory('localhost', 8000, 'v1', ttl=1, ttr=1, timeout=30)
        instance = library.bind_instance('test_api')  # update cache and call SD
        self.assertEquals('uri_test', instance.uri)
        time.sleep(1.1)  # after 1 second the cache should be refreshed
        instance = library.bind_instance('test_api')  # sd return Timeout and we return cached
        self.assertEquals('uri_test', instance.uri)
        self.requestGetMock.assert_has_calls([call(ANY, timeout=30, auth=ANY, params=ANY),
                                              call(ANY, timeout=30, auth=ANY, params=ANY)])
        self.assertEquals(2, self.requestGetMock.call_count, "SD called more than 3 times")

    def test_get_endpoints_ttr_and_ttl_expired_SD_Unavailable_should_return_exception(self):
        sdRespMock = MagicMock(name='sdRespMockRefresh')
        sdRespMock.status_code = 200
        returns = [
        {
          "class_name": "test_api",
          "uri": "uri_test_ttl",
          "version": "1.0",
          "environment": "production",
          "attributes": {"ob": "oba"}
        }, Timeout('SD unavailable')]

        def side_effect_calls(*args):
            result = returns.pop(0)
            if isinstance(result, Exception):
                raise result
            return result

        sdRespMock.json.side_effect = side_effect_calls
        self.requestGetMock.return_value = sdRespMock
        library = ServiceDirectory('localhost', 8000, 'v1', ttr=0.1, ttl=1.0 / 3600, timeout=30)
        instance = library.bind_instance('test_api')  # update cache and call SD
        self.assertEquals('uri_test_ttl', instance.uri)
        time.sleep(1.1)  # after 1.1 seconds ttr and ttl are expired
        self.assertRaises(ConnectionException, library.bind_instance, 'test_api')
        self.requestGetMock.assert_has_calls([call(ANY, timeout=30, auth=ANY, params=ANY),
                                              call(ANY, timeout=30, auth=ANY, params=ANY)])
        self.assertEquals(2, self.requestGetMock.call_count, "SD called more than 3 times")

    def test_get_endpoints_ttl_expired_SD_Unavailable_should_return_new_value(self):
        sdRespMock = MagicMock(name='sdRespMockRefresh')
        sdRespMock.status_code = 200
        returns = [
        {
          "class_name": "test_api",
          "uri": "uri_test_ttl",
          "version": "1.0",
          "environment": "production",
          "attributes": {"ob": "oba"}
        }, Timeout('SD unavailable'),
        {
          "class_name": "test_api",
          "uri": "uri_test_available",
          "version": "1.0",
          "environment": "production",
          "attributes": {"ob": "oba"}
        }]

        def side_effect_calls(*args):
            result = returns.pop(0)
            if isinstance(result, Exception):
                raise result
            return result

        sdRespMock.json.side_effect = side_effect_calls
        self.requestGetMock.return_value = sdRespMock
        library = ServiceDirectory('localhost', 8000, 'v1', ttr=0.1, ttl=1.0 / 3600, timeout=30)
        instance = library.bind_instance('test_api')  # update cache and call SD
        self.assertEquals('uri_test_ttl', instance.uri)
        time.sleep(1.1)  # after 1.1 seconds ttr and ttl are expired, we get Exception
        self.assertRaises(ConnectionException, library.bind_instance, 'test_api')
        # Now SD becomes available and the cache element does not exist, SD called
        instance = library.bind_instance('test_api')  # fill cache and call SD
        self.assertEquals('uri_test_available', instance.uri)
        # now is in the cache again
        instance = library.bind_instance('test_api')  # fill cache and call SD
        self.assertEquals('uri_test_available', instance.uri)
        self.requestGetMock.assert_has_calls([call(ANY, timeout=30, auth=ANY, params=ANY),
                                              call(ANY, timeout=30, auth=ANY, params=ANY),
                                              call(ANY, timeout=30, auth=ANY, params=ANY)])
        self.assertEquals(3, self.requestGetMock.call_count, "SD called more than 3 times")

    def test_get_endpoints_with_context_cached_should_return_from_cache(self):
        library = ServiceDirectory('localhost', 8000, 'v1')
        instance = library.bind_instance('test_api',
                                    context={'ob': 'oba', 'premium': True})
        self.assertEquals('test_api', instance.class_name)
        self.assertEquals('uri_test', instance.uri)
        self.assertEquals({"ob": "oba"}, instance.attributes)

        # If we call get_endPoinst we must have the value cached
        instance = library.bind_instance('test_api',
                                          context={'premium': True, 'ob': 'oba'})
        self.assertEquals('test_api', instance.class_name)
        self.assertEquals('uri_test', instance.uri)
        self.assertEquals({"ob": "oba"}, instance.attributes)
        self.requestGetMock.assert_called_once_with(ANY, timeout=30, auth=ANY, params=ANY)

    def test_get_endpoints_uncached_SD_timeout_should_raise_conn_exception(self):
        self.requestGetMock.side_effect = Timeout()
        library = ServiceDirectory('localhost', 8000, 'v1', ttr=0.1, ttl=1.0 / 3600, timeout=30)
        self.assertRaises(ConnectionException, library.bind_instance, 'test_api')
        self.requestGetMock.assert_called_once_with(ANY, timeout=30, auth=ANY, params=ANY)

    def test_get_endpoints_uncached_SD_conn_error_should_raise_conn_exception(self):
        self.requestGetMock.side_effect = TooManyRedirects()
        library = ServiceDirectory('localhost', 8000, 'v1', ttr=0.1, ttl=1.0 / 3600, timeout=30)
        self.assertRaises(ConnectionException, library.bind_instance, 'test_api')
        self.requestGetMock.assert_called_once_with(ANY, timeout=30, auth=ANY, params=ANY)

    def test_get_endpoints_bad_json_resp_SD_should_raise_remote(self):
        sdRespMock = MagicMock(name='sdRespMockRefresh')
        sdRespMock.status_code = 200

        sdRespMock.json.return_value = {
          "class_name": "api"
        }
        self.requestGetMock.return_value = sdRespMock
        library = ServiceDirectory('localhost', 8000, 'v1', ttr=0.1, ttl=1.0 / 3600, timeout=30)
        self.assertRaises(RemoteException, library.bind_instance, 'test_api')

    def test_get_endpoints_error_resp_SD_should_raise_remote(self):
        sdRespMock = MagicMock(name='sdRespMockRefresh')
        sdRespMock.status_code = 400

        sdRespMock.json.return_value = {
          "exceptionText": "Bidning not found",
          "excetpionId": "SVC0000"
        }
        self.requestGetMock.return_value = sdRespMock
        library = ServiceDirectory('localhost', 8000, 'v1', ttr=0.1, ttl=1.0 / 3600, timeout=30)
        self.assertRaises(RemoteException, library.bind_instance, 'test_api')

    def test_get_endpoints_invalid_context_should_raise_sdLibrary(self):
        library = ServiceDirectory('localhost', 8000, 'v1', ttr=0.1, ttl=1.0 / 3600, timeout=30)
        self.assertRaises(SDLibraryException, library.bind_instance, 'test_api', 'invalid_context')

if __name__ == "__main__":
    unittest.main(argv=unittest.sys.argv + ['--verbose'])
