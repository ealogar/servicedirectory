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

import sqlite3
from common.rest_utils import RestUtils
from common.api_utils import APIUtils
from common.mongo_utils import MongoUtils
from common.web_utils import WebUtils

rest_utils = RestUtils()
api_utils = APIUtils()
mongo_utils = MongoUtils()
web_utils = WebUtils()


@step('I go to "(.*?)"$')
def goto(step, url):
    web_utils.goto(step, url)


@step('I should be at "(.*?)"$')
def should_be_at(step, url):
    web_utils.should_be_at(step, url)


@step('The element with id of "(.*?)" contains placeholder "(.*?)"$')
def placeholder_contains(step, element_id, value):
    web_utils.placeholder_contains(step, element_id, value)


@step('And user "([^"]*)" is not registered')
def user_is_not_registered(step, username):
    conn = sqlite3.connect('../../src/web-admin-sd/sd-web/sd.db')
    c = conn.cursor()
    for row in c.execute('SELECT username FROM auth_user'):
        if row[0] == username:
            assert False, 'The user username is already registered, and it shouldnt'
            break


@step('And user "([^"]*)" is registered')
def user_is_registered(step, username):
    conn = sqlite3.connect('../../src/web-admin-sd/sd-web/sd.db')
    c = conn.cursor()
    for row in c.execute('SELECT username FROM auth_user'):
        if row[0] == username:
            break
    else:
        assert False, 'The user username is not registered, and it should'


@step(u'the DB is working')
def the_db_is_working(step):
    mongo_utils.the_db_is_working(step)


@step(u'the DB has stopped working')
def the_db_has_stopped_working(step):
    mongo_utils.the_db_has_stopped_working(step)


@step(u'I should see a form with csrf token')
def i_should_see_a_form_with_csrf_token(step):
    web_utils.should_see_a_form_with_csrf_token(step)


@step(u'I fill in "(.*)" with (.*)$')
def i_fill_in(step, field, value):
    web_utils.fill_in(step, field, value)
