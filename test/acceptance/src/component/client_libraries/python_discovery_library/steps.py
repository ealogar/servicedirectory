# -*- coding: utf-8 -*-
'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
from lettuce import step
from common.python_lib_utils import PythonLibUtils
from component.common.mock_utils import MockUtils
import time

python_lib_utils = PythonLibUtils()
mock_utils = MockUtils()


@step(u'the SD mock is working')
def the_sd_mock_is_working(step):
    mock_utils.start_sd_mock()


@step(u'the SD mock is not working')
def the_sd_mock_is_not_working(step):
    mock_utils.stop_sd_mock()


@step(u'I wait for (\d+) seconds')
def wait_for_seconds(step, seconds):
    time.sleep(seconds)


@step(u'I instantiate the library with values (\d+):')
def instantiate_the_library_with_values(step, config_index):
    python_lib_utils.instantiate_the_library_with_values(step, config_index)


@step(u'I configure the SD mock to get the request to (.*) and send a response of type (\d+) with data (.*):')
def get_request_and_send_response_of_type_with_data(step, request, status_code, r_index):
    mock_utils.get_request_and_send_response_of_type_with_data(step, request, status_code, response_index=r_index)


@step(u'I configure the SD mock to get the request to (.*) and send a response of type (\d+) ' +
      'with a delay of (\d+) seconds and dataset:')
def get_request_and_send_response_of_type_with_delay_and_dataset(step, request, status_code, delay):
    mock_utils.get_request_and_send_response_of_type_with_data(step, request, status_code, delay=delay)


@step(u'I configure the SD mock to get the request to (.*) and send a response of type (\d+) with dataset:')
def get_request_and_send_response_of_type_with_dataset(step, request, status_code):
    mock_utils.get_request_and_send_response_of_type_with_data(step, request, status_code)


@step(u'I use the library to search for endpoints with data (.*):')
def i_use_the_library_to_search_for_endpoints_with_data(step, response_index):
    python_lib_utils.search_for_endpoints_with_data(step, response_index)


@step(u'I get a result set of size (\d+)')
def get_a_resultset_of_size(step, size):
    python_lib_utils.get_a_resultset_of_size(step, size)


@step(u'the result set contains the endpoint (\d+) in position (\d+):')
def the_resultset_contains_endpoint_in_position(step, endpoint_index, position):
    python_lib_utils.the_resultset_contains_endpoint(step, endpoint_index, position)


@step(u'the result set contains the endpoint (\d+):')
def the_resultset_contains_endpoint(step, endpoint_index):
    python_lib_utils.the_resultset_contains_endpoint(step, endpoint_index)


@step(u'I get a exception of type (\w+)')
def i_get_a_exception_of_type(step, exception_type):
    python_lib_utils.get_a_exception_of_type(step, exception_type)
