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


@step(u'I send to (.*) the instance data (\d+):')
def i_send_to_url_the_instance_data(step, url, class_index):
    api_utils.send_to_url_the_instance_data(step, url, class_index)


@step(u'a class has already been published with data (\d+):')
def a_class_has_already_been_published_with_data(step, old_class_index):
    api_utils.a_class_has_already_been_published_with_data(step, old_class_index)


@step(u'a class has not already been published with data (.*):')
def a_class_has_not_already_been_published_with_data(step, old_class_index):
    api_utils.a_class_has_not_already_been_published_with_data(step, old_class_index)


@step(u'an instance has already been published with data (\d+):')
def an_instance_has_already_been_published_with_data(step, old_instance_index):
    api_utils.an_instance_has_already_been_published_with_data(step, old_instance_index)


@step(u'the response contains the instance data')
def the_response_contains_the_instance_data(step):
    api_utils.the_response_contains_the_instance_data()


@step(u'the location returns the instance data')
def the_location_returns_the_instance_data(step):
    api_utils.the_url_returns_the_instance_data(step, world.location)


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


@step(u'the result set contains the instance (\d+) in position (\d+):')
def the_resultset_contains_instance_in_position(step, instance_index, position):
    api_utils.the_resultset_contains_instance_in_position(step, instance_index, position)


@step(u'the result set contains the instance (\d+):')
def the_resultset_contains_instance(step, instance_index):
    api_utils.the_resultset_contains_instance_in_position(step, instance_index)


@step(u'And the previous bindings are pusblished for the context (\d+):')
def and_the_previous_bindings_are_pusblished_for_the_context_operation_index(step, context_index):
    i_send_to_url_the_rule_data(step, "$base_api_url/$classes_url/$class_name/$request_context_rules_url",\
                                 context_index)


@step(u'the exceptionText contains (\d+)')
def the_exceptiontext_contains_exceptiontext(step, exceptionText_index):
    api_utils.the_exceptiontext_contains_exceptiontext(step, exceptionText_index)


@step(u'the instance published in position (\d+) has been deleted')
def the_instance_published_has_been_deleted(step, position):
    i_delete_url(step, "$base_api_url/$classes_url/$class_name/$instances_url/" + api_utils.get_instance_id(position))


@step(u'I delete resource (\d+):')
def i_delete_resource(step, resource_index):
    i_delete_url(step, step.hashes[int(resource_index)]["resource"])


@step(u'I delete (.*)')
def i_delete_url(step, url):
    rest_utils.delete_url(step, url)


@step(u'the user performing the operation is (\d+)')
def the_user_performing_the_operation_is(step, user_index):
    world.request_user = step.hashes[int(user_index)]["username"]
    world.request_password = step.hashes[int(user_index)]["password"]
    assert True


@step(u'I send to (.*) the user data (\d+):')
def i_send_to_url_the_user_data(step, url, user_data_index):
    api_utils.send_to_url_the_user_data(step, url, user_data_index)


@step(u'I update (.*) with the user data (\d+):')
def i_update_url_with_the_user_data(step, url, user_data_index):
    api_utils.send_to_url_the_user_data(step, url + step.hashes[int(user_data_index)]["username"], user_data_index)


@step(u'the response contains the user data')
def the_response_contains_the_user_data(step):
    api_utils.the_response_contains_the_user_data()


@step(u'the location returns the user data')
def the_location_returns_the_user_data(step):
    api_utils.the_url_returns_the_user_data(step, world.location)


@step(u'a user has already been created with data (\d+)')
def a_user_has_already_been_created_with_data(step, user_data_index):
    i_send_to_url_the_user_data(step, "$base_api_url/$users_url", user_data_index)


@step(u'I get a success response of type (\d+)')
def i_get_a_success_response_of_type(step, status_code):
    rest_utils.get_a_success_response_of_type(step, status_code)


@step(u'the URL (.*) returns the error code (\d+) with error code (\w+)')
def the_url_returns_an_error_of_type_with_error_code(step, url, status_code, error_code):
    api_utils.the_url_returns_an_error_of_type_with_error_code(step, url, status_code, error_code)


@step(u'no users are previously created in the system')
def no_users_are_previously_created_in_the_system(step):
    test_utils.reset_world()
    mongo_utils.reset_mongo()
