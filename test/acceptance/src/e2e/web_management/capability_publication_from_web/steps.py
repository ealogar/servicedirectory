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


@step('The element with id of "(.*?)" contains placeholder "(.*?)"$')
def placeholder_contains(step, element_id, value):
    web_utils.placeholder_contains(step, element_id, value)


@step(u'I should see a link that contains the text "(.*)" and the url "(.*)"')
def should_see_a_link_with_text_and_url(step, text, url):
    web_utils.should_see_a_link_with_text_and_url(step, text, url)


@step(u'I store in world the capability "(.*)", "(.*)", "(.*)"')
def i_store_in_world_the_capability(step, api_name, description='', default_version=''):
    world.capability = {"api_name": api_name, "description": description, "default_version": default_version}


@step(u'the DB is working')
def the_db_is_working(step):
    mongo_utils.the_db_is_working(step)


@step(u'the DB has stopped working')
def the_db_has_stopped_working(step):
    mongo_utils.the_db_has_stopped_working(step)


@step(u'the DB has no capabilities already published')
def the_db_has_no_capabilities_already_published(step):
    pass    # the database is cleaned before each scenario


@step(u'the DB contains the capability data')
def the_db_contains_the_capability_data(step):
    api_utils.the_db_contains_the_capability_data(step)


@step(u'the DB does not have the capability data')
def the_db_does_not_have_the_capability_data(step):
    api_utils.the_db_does_not_have_the_capability_data(step)


@step(u'a capability has already been published with data (\d+):')
def a_capability_has_already_been_published_with_data(step, old_cap_index):
    api_utils.a_capability_has_already_been_published_with_data(step, old_cap_index)


@step(u'the DB contains just the old capability data')
def the_db_contains_just_old_capability_data(step):
    api_utils.the_db_contains_just_old_capability_data(step)


@step(u'the URL (.*) returns the capability data')
def the_url_returns_the_updated_capability_data(step, url):
    api_utils.the_url_returns_the_capability_data(step, url)


@step(u'I should see a form with csrf token')
def i_should_see_a_form_with_csrf_token(step):
    web_utils.should_see_a_form_with_csrf_token(step)
