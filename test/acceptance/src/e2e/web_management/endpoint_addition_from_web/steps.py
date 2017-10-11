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


@step('The element with id of "(.*?)" contains "(.*?)"$')
def contains(step, element_id, value):
    web_utils.contains(step, element_id, value)


@step('The element with id of "(.*?)" contains placeholder "(.*?)"$')
def placeholder_contains(step, element_id, value):
    web_utils.placeholder_contains(step, element_id, value)


@step(u'I should see a link that contains the text "(.*)" and the url "(.*)"')
def should_see_a_link_with_text_and_url(step, text, url):
    web_utils.should_see_a_link_with_text_and_url(step, text, url)


@step(u'I should see "(.*)"')
def should_see(step, text):
    web_utils.should_see(step, text)


@step('I check "(.*?)" with "(.*?)"')
def check(step, id_element, status):
    web_utils.check(step, id_element, status)


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


@step(u'the DB contains just the old capability data')
def the_db_contains_just_old_capability_data(step):
    api_utils.the_db_contains_just_old_capability_data(step)


@step(u'the DB contains the endpoint data')
def the_db_contains_the_endpoint_data(step):
    api_utils.the_db_contains_the_endpoint_data(step)


@step(u'the DB does not have the endpoint data')
def the_db_does_not_have_the_endpoint_data(step):
    api_utils.the_db_does_not_have_the_endpoint_data(step)


@step(u'the DB contains just the old endpoint data')
def the_db_contains_just_old_endpoint_data(step):
    api_utils.the_db_contains_just_old_endpoint_data(step)


@step(u'I store in world the endpoint "(.*)", "(.*)", "(.*)", "(.*)"')
def and_i_store_in_world_the_endpoint(step, url, version, premium=False, ob=''):
    """Replace the values."""
    if "$url" in url:
        old_url = world.old_capability[world.config["keys"]["url"]]
    else:
        old_url = url
    if "$version" in version:
        old_version = world.old_capability[world.config["keys"]["version"]]
    else:
        old_version = version
    if "$premium" in premium:
        old_premium = world.old_capability[world.config["keys"]["premium"]]
    else:
        old_premium = premium
    if "$ob" in ob:
        old_ob = world.old_capability[world.config["keys"]["ob"]]
    else:
        old_ob = ob
    world.endpoint = {"url": old_url, "version": old_version, "premium": old_premium, "ob": old_ob}


@step(u'endpoints should be ordered by version')
def endpoints_should_be_ordered_by_version(step):
    xpathtr = "//table/tbody/tr"
    rows = len(world.browser.find_elements_by_xpath(xpathtr))
    versions = []
    for i in range(1, rows + 1):
        xpathversion = "//table/tbody/tr[%s]/td[2]" % i
        versions.append(world.browser.find_element_by_xpath(xpathversion).text)
    assert sorted(versions, reverse=True) == versions
