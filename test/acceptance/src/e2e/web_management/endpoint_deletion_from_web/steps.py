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
from common.mongo_utils import MongoUtils
from common.web_utils import WebUtils

rest_utils = RestUtils()
api_utils = APIUtils()
mongo_utils = MongoUtils()
web_utils = WebUtils()


@step(u'the admin is logged')
def the_admin_is_logged(step):
    web_utils.login_admin(step)


@step('I go to "(.*?)"$')
def goto(step, url):
    web_utils.goto(step, url)


@step(u'I press "(.*?)"$')
def i_press(step, element_id):
    web_utils.press(step, element_id)


@step(u'I should see "(.*)"')
def should_see(step, text):
    web_utils.should_see(step, text)


@step(u'I should see a form with csrf token')
def i_should_see_a_form_with_csrf_token(step):
    web_utils.should_see_a_form_with_csrf_token(step)


@step(u'the DB is working')
def the_db_is_working(step):
    mongo_utils.the_db_is_working(step)


@step(u'the DB has stopped working')
def the_db_has_stopped_working(step):
    mongo_utils.the_db_has_stopped_working(step)


@step(u'a capability has already been published with data (\d+):')
def a_capability_has_already_been_published_with_data(step, old_cap_index):
    api_utils.a_capability_has_already_been_published_with_data(step, old_cap_index)


@step(u'an endpoint has already been published with data (\d+):')
def an_endpoint_has_already_been_published_with_data(step, old_endpoint_index):
    api_utils.an_endpoint_has_already_been_published_with_data(step, old_endpoint_index)


@step(u'I store in world the endpoint with data (\d+):')
def and_i_store_in_world_the_endpoint(step, endpoint_index):
    world.endpoint = step.hashes[int(endpoint_index)]


@step(u'the URL (.*) returns the endpoint data')
def the_url_returns_the_endpoint_data(step, url):
    api_utils.the_url_returns_the_endpoint_data(step, url)


@step(u'the URL (.*) returns the error code (\d+) with error code (\w+)')
def the_url_returns_an_error_of_type_with_error_code(step, url, status_code, error_code):
    api_utils.the_url_returns_an_error_of_type_with_error_code(step, url, status_code, error_code)
