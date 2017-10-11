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


@step(u'I put in (.*) the data (.*)')
def i_send_to_url_the_data(step, url, data):
    rest_utils.put_in_url_the_data(step, url, data)


@step(u'I put in (.*) the instance data (\d+):')
def i_put_in_url_the_instance_data(step, url, instance_index):
    api_utils.put_in_url_the_instance_data(step, url, instance_index)


@step(u'I try to partially update in (.*) the instance data (\d+):')
def i_try_to_partially_update_the_instance_data(step, url, instance_index):
    api_utils.send_to_url_the_class_data(step, url, instance_index)


@step(u'I get a success response of type (\d+) with the updated instance data')
def i_get_a_success_response_of_type_with_updated_instance_data(step, status_code):
    api_utils.i_get_a_success_response_of_type_with_updated_instance_data(step, status_code)


@step(u'I get an error response of type (\d+) with error code (\w+)')
def i_get_an_error_response_of_type_with_error_code(step, status_code, error_code):
    rest_utils.get_an_error_response_of_type_with_error_code(step, status_code, error_code)


@step(u'a class has already been published with data (\d+):')
def a_class_has_already_been_published_with_data(step, old_class_index):
    api_utils.a_class_has_already_been_published_with_data(step, old_class_index)


@step(u'an instance has already been published with data (\d+):')
def an_instance_has_already_been_published_with_data(step, old_instance_index):
    api_utils.an_instance_has_already_been_published_with_data(step, old_instance_index)


@step(u'an instance has not already been published with data (.*):')
def an_instance_has_not_already_been_published_with_data(step, old_instance_index):
    api_utils.an_instance_has_not_already_been_published_with_data(step, old_instance_index)


@step(u'the URL (.*) returns the updated instance data')
def the_url_returns_the_updated_instance_data(step, url):
    api_utils.the_url_returns_the_instance_data(step, url)


@step(u'the exceptionText contains (\d+)')
def the_exceptiontext_contains_exceptiontext(step, exceptionText_index):
    api_utils.the_exceptiontext_contains_exceptiontext(step, exceptionText_index)


@step(u'the user performing the operation is:')
def the_user_performing_the_operation_is(step):
    test_utils.reset_world()
    world.request_user = step.hashes[0]["username"]
    world.request_password = step.hashes[0]["password"]
    assert True
