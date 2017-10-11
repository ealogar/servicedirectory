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
from common.rest_utils import RestUtils
from common.api_utils import APIUtils
from common.mongo_utils import MongoUtils

rest_utils = RestUtils()
api_utils = APIUtils()
mongo_utils = MongoUtils()


@step(u'the DB is working')
def the_db_is_working(step):
    mongo_utils.the_db_is_working(step)


@step(u'the DB has stopped working')
def the_db_has_stopped_working(step):
    mongo_utils.the_db_has_stopped_working(step)


@step(u'a capability has already been published with data (\d+):')
def a_capability_has_already_been_published_with_data(step, old_cap_index):
    api_utils.a_capability_has_already_been_published_with_data(step, old_cap_index)


@step(u'a capability has not already been published with data (.*):')
def a_capability_has_not_already_been_published_with_data(step, old_cap_index):
    api_utils.a_capability_has_not_already_been_published_with_data(step, old_cap_index)


@step(u'an endpoint has already been published with data (\d+):')
def an_endpoint_has_already_been_published_with_data(step, old_endpoint_index):
    api_utils.an_endpoint_has_already_been_published_with_data(step, old_endpoint_index)


@step(u'I request the resource (.*)')
def request_the_resource(step, url):
    rest_utils.request_the_resource(step, url)


@step(u'I request the resource (.*) with parameters (\d+):')
def request_the_resource_with_parameters(step, url, params_index):
    rest_utils.request_the_resource(step, url, params_index)


@step(u'I get a success response of type (\d+) with a result set of size (\d+)')
def get_a_success_response_of_type_with_resultset_of_size(step, status_code, size):
    rest_utils.get_a_success_response_of_type_with_resultset_of_size(step, status_code, size)


@step(u'I get an error response of type (\d+) with error code (\w+)')
def i_get_an_error_response_of_type_with_error_code(step, status_code, error_code):
    rest_utils.get_an_error_response_of_type_with_error_code(step, status_code, error_code)


@step(u'the result set contains the endpoint (\d+) in position (\d+):')
def the_resultset_contains_endpoint_in_position(step, endpoint_index, position):
    api_utils.the_resultset_contains_endpoint_in_position(step, endpoint_index, position)


@step(u'the result set contains the endpoint (\d+):')
def the_resultset_contains_endpoint(step, endpoint_index):
    api_utils.the_resultset_contains_endpoint_in_position(step, endpoint_index)
