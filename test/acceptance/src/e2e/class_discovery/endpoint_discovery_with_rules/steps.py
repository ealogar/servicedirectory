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
from lettuce import step, world
from common.rest_utils import RestUtils
from common.api_utils import APIUtils
from common.test_utils import TestUtils
from common.mongo_utils import MongoUtils

rest_utils = RestUtils()
test_utils = TestUtils()
api_utils = APIUtils()
mongo_utils = MongoUtils()


@step(u'the DB is working')
def the_db_is_working(step):
    mongo_utils.the_db_is_working(step)


@step(u'the DB has stopped working')
def the_db_has_stopped_working(step):
    mongo_utils.the_db_has_stopped_working(step)


@step(u'I send to (.*) the data (.*)')
def i_send_to_url_the_data(step, url, data):
    rest_utils.send_to_url_the_data(step, url, data)


@step(u'I get a success response of type (\d+) with location (.+):')
def i_get_a_success_response_of_type_with_location(step, status_code, location_index):
    rest_utils.get_a_success_response_of_type_with_location(step, status_code, location_index)


@step(u'I get an error response of type (\d+) with error code (\w+)')
def i_get_an_error_response_of_type_with_error_code(step, status_type, error_code):
    rest_utils.get_an_error_response_of_type_with_error_code(step, status_type, error_code)


@step(u'I send to (.*) the endpoint data (\d+):')
def i_send_to_url_the_endpoint_data(step, url, cap_index):
    api_utils.send_to_url_the_endpoint_data(step, url, cap_index)


@step(u'a capability has already been published with data (\d+):')
def a_capability_has_already_been_published_with_data(step, old_cap_index):
    api_utils.a_capability_has_already_been_published_with_data(step, old_cap_index)


@step(u'a capability has not already been published with data (.*):')
def a_capability_has_not_already_been_published_with_data(step, old_cap_index):
    api_utils.a_capability_has_not_already_been_published_with_data(step, old_cap_index)


@step(u'an endpoint has already been published with data (\d+):')
def an_endpoint_has_already_been_published_with_data(step, old_endpoint_index):
    api_utils.an_endpoint_has_already_been_published_with_data(step, old_endpoint_index)


@step(u'the response contains the endpoint data')
def the_response_contains_the_endpoint_data(step):
    api_utils.the_response_contains_the_endpoint_data()


@step(u'the location returns the endpoint data')
def the_location_returns_the_endpoint_data(step):
    api_utils.the_url_returns_the_endpoint_data(step, world.location)


@step(u'I send to (.*) the rule data (\d+):')
def i_send_to_url_the_rule_data(step, url, rule_index):
    api_utils.send_to_url_the_rule_data(step, url, rule_index)


@step(u'the response contains the rule data')
def the_response_contains_the_rule_data(step):
    api_utils.the_response_contains_the_rule_data()


@step(u'the location returns the rule data')
def the_location_returns_the_rule_data(step):
    api_utils.the_url_returns_the_rule_data(step, world.location)


@step(u'the following bindings rules are available (.*):')
def the_following_bindings_rules_are_available(step, operation_index):
    api_utils.the_following_bindings_rules_are_avalilabe(step, operation_index)


@step(u'there is a context rule already been published with data (\d+):')
def there_is_a_context_rule_already_been_published_with_data(step, old_rule_index):
    api_utils.there_is_a_context_rule_already_been_published_with_data(step, old_rule_index)


@step(u'the following bindings in (\d+) are available for the context rules:')
def and_the_following_bindings_in_bindings_index_are_available_for_the_context_rules(step, binding_index):
    api_utils.the_following_bindings_are_available_for_the_context_rules(step, binding_index)


@step(u'I request the resource (.*)')
def request_the_resource(step, url):
    rest_utils.request_the_resource(step, url)


@step(u'I request the resource (.*) with parameters (\d+):')
def request_the_resource_with_parameters(step, url, params_index):
    rest_utils.request_the_resource(step, url, params_index)


@step(u'I get a success response of type (\d+) with a result set of size (\d+)')
def get_a_success_response_of_type_with_resultset_of_size(step, status_code, size):
    rest_utils.get_a_success_response_of_type_with_resultset_of_size(step, status_code, size)


@step(u'the result set contains the endpoint (\d+) in position (\d+):')
def the_resultset_contains_endpoint_in_position(step, endpoint_index, position):
    api_utils.the_resultset_contains_endpoint_in_position(step, endpoint_index, position)


@step(u'the result set contains the endpoint (\d+):')
def the_resultset_contains_endpoint(step, endpoint_index):
    api_utils.the_resultset_contains_endpoint_in_position(step, endpoint_index)


@step(u'And the previous bindings are pusblished for the context (\d+):')
def and_the_previous_bindings_are_pusblished_for_the_context_operation_index(step, context_index):
    i_send_to_url_the_rule_data(step, "$base_api_url/$apis_url/$api_name/$request_context_rules_url", context_index)


@step(u'the exceptionText contains (\d+)')
def the_exceptiontext_contains_exceptiontext(step, exceptionText_index):
    api_utils.the_exceptiontext_contains_exceptiontext(step, exceptionText_index)


@step(u'the endpoint published in position (\d+) has been deleted')
def the_endpoint_published_has_been_deleted(step, position):
    i_delete_url(step, "$base_api_url/$apis_url/$api_name/$endpoints_url/" + api_utils.get_endpoint_id(position))


@step(u'I delete (.*)')
def i_delete_url(step, url):
    rest_utils.delete_url(step, url)


@step(u'the user performing the operation is:')
def the_user_performing_the_operation_is(step):
    test_utils.reset_world()
    world.request_user = step.hashes[0]["username"]
    world.request_password = step.hashes[0]["password"]
    assert True
