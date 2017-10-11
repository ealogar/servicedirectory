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
from common.mongo_utils import MongoUtils
from common.web_utils import WebUtils

mongo_utils = MongoUtils()
web_utils = WebUtils()


@step(u'the admin is logged')
def the_admin_is_logged(step):
    web_utils.login_admin(step)


@step('I go to "(.*?)"$')
def goto(step, url):
    web_utils.goto(step, url)


@step('I click "(.*?)"$')
def click(step, text):
    web_utils.click(step, text)


@step('I should be at "(.*?)"$')
def should_be_at(step, url):
    web_utils.should_be_at(step, url)


@step(u'the DB is working')
def the_db_is_working(step):
    mongo_utils.the_db_is_working(step)


@step(u'The title should be "([^"]*)"')
def the_title_should_be(step, title):
    web_utils.the_title_should_be(step, title)


@step(u'I should see a link that contains the text "(.*)" and the url "(.*)"')
def should_see_a_link_with_text_and_url(step, text, url):
    web_utils.should_see_a_link_with_text_and_url(step, text, url)
