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
import platform
import time
from lettuce import world
from string import Template
from selenium import webdriver
import lettuce_webdriver.webdriver
from lettuce_webdriver.util import AssertContextManager
from lettuce_webdriver.util import assert_true
from lettuce_webdriver.util import find_field
from urlparse import urlparse
import subprocess
import time
from common.test_utils import TestUtils

test_utils = TestUtils()

class WebUtils(object):

    def start_web(self):
        """
        Start the web if not already started and store the process in the world.
        """
        if not hasattr(world, "web_working") or world.web_working == False:
            run_command_temp = Template(" ".join([world.config["environment"]["python_alias"],
                                                 world.config["web_server"]["run_command_params"]]))
            run_command = run_command_temp.safe_substitute(env=world.config["environment"]["name"])
            out = open(world.config["web_server"]["out_file"], 'w')
            err = open(world.config["web_server"]["err_file"], 'w')
            world.web_process = subprocess.Popen(run_command.split(), stdout=out, stderr=err)
            time.sleep(1)
            world.web_working = True

    def stop_web(self):
        """
        Stop the web if not already stopped.
        """
        if hasattr(world, "web_working") and world.web_working == True:
            test_utils.kill_process(world.web_process.pid)
            time.sleep(0.5)
            world.web_working = False

    def web_is_working(self):
        """
        Check whether the Web is working.
        """
        if hasattr(world, "web_working") and world.web_working == True:
            return True
        else:
            return False

    def setup_browser(self):
        """
        Set up the browser with Firefox/Chrome profile
        """
        if world.config["browser_prefs"]["browser"] == "chrome":
            if platform.system() == "Windows":
                chromedriver = world.config["browser_prefs"]["chromedriver_path_windows"]
            elif platform.system() == "Linux":
                chromedriver = world.config["browser_prefs"]["chromedriver_path"]
            service_log_path = world.config["browser_prefs"]["chromedriver_log_path"]
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            try:
                world.browser = webdriver.Chrome(chromedriver, chrome_options=options,
                                                 service_log_path=service_log_path)
            except:
                assert False, "Chrome driver can not be launched. Platform chosen: %s. "\
                    "Path given in properties: %s " % (platform.system(), chromedriver)
        else:
            try:
                world.browser = webdriver.Firefox()
                world.browser.maximize_window()
            except:
                assert False, "Firefox driver can not be launched. Platform chosen: %s " % platform.system()

    def goto(self, step, url):
        """
        Navigate to the given url.
        :param step: current Lettuce step.
        :param url: destination URL.
        """
        url = self.parse_variables(url)
        with AssertContextManager(step):
            world.browser.get(url)

    def click(self, step, text):
        """
        Click on the given element, identified by its text.
        :param step: current Lettuce step.
        :param text: text of the element to be clicked.
        """
        text = self.parse_variables(text)
        lettuce_webdriver.webdriver.click(step, text)

    def press(self, step, element_id):
        """
        Click on the given element, identified by its id.
        :param step: current Lettuce step.
        :param element_id: id of the element to be clicked.
        """
        element_id = self.parse_variables(element_id)
        elem = world.browser.find_element_by_xpath('//*[@id="%s"]' % element_id)
        elem.click()
        time.sleep(1)

    def should_be_at(self, step, url):
        """
        Check the current url of the navigator.
        :param step: current Lettuce step.
        :param url: expected url of the navigator.
        """
        url = self.parse_variables(url)
        lettuce_webdriver.webdriver.url_should_be(step, url)

    def should_see(self, step, text):
        """
        Check that a given text is shown in the current page.
        :param step: current Lettuce step.
        :param text: expected text to be shown on the current page.
        """
        time.sleep(0.8)
        text = self.parse_variables(text)
        lettuce_webdriver.webdriver.should_see(step, text)

    def should_not_see(self, step, text):
        """
        Check that a given text is not shown in the current page.
        :param step: current Lettuce step.
        :param text: expected text not to be shown on the current page.
        """
        time.sleep(0.2)
        text = self.parse_variables(text)
        lettuce_webdriver.webdriver.should_not_see(step, text)

    def should_see_a_link_with_text_and_url(self, step, text, url):
        """
        Check that a link with the given text and url link is shown in the current page.
        :param step: current Lettuce step.
        :param text: expected text of the link.
        :param url: expected url link of the link.
        """
        text = self.parse_variables(text)
        if "$base_web_url" in url:
            temp_url = urlparse(world.config["django"]["base_web_url"])
            base_web_url = temp_url.path
        else:
            base_web_url = None
        temp = Template(url)
        url = temp.safe_substitute(base_web_url=base_web_url)
        url = self.parse_variables(url)
        return world.browser.find_element_by_xpath('//a[@href="%s"][contains(., "%s")]' % (url, text))

    def should_see_a_form_with_csrf_token(self, step):
        """
        Check that a csrf token is present on the form of the current page.
        :param step: current Lettuce step.
        """
        time.sleep(0.5)
        return world.browser.find_element_by_xpath('//*[@name="csrfmiddlewaretoken"]')

    def check(self, step, id_element, status):
        """
        Click on the checkbox identified but the given id
        depending on the given status.
        :param step: current Lettuce step.
        :param id_element: id of the checkbox element.
        :param status: status of the checkbox to be set.
        """
        with AssertContextManager(step):
            check_box = find_field(world.browser, 'checkbox', id_element)
            if not check_box.is_selected() and status == 'True':
                check_box.click()
            if check_box.is_selected() and status == 'False':
                check_box.click()

    def contains(self, step, element_id, value):
        """
        Check that the element identified but the given id
        contains the value given.
        :param step: current Lettuce step.
        :param id_element: id of the element to be checked.
        :param value: expected value of the element to be checked.
        """
        value = self.parse_variables(value)
        lettuce_webdriver.webdriver.element_contains(step, element_id, value)

    def placeholder_contains(self, step, element_id, value):
        """
        Check that the element identified but the given id
        contains the placeholder given.
        :param step: current Lettuce step.
        :param id_element: id of the element to be checked.
        :param value: expected placeholder of the element to be checked.
        """
        elem = world.browser.find_element_by_xpath('//*[@id="%s"]' % element_id)
        assert_true(step, value in elem.get_attribute('placeholder'))

    def login_admin(self, step):
        """
        Log in the Service Directory site using the default credentials.
        :param step: current Lettuce step.
        """
        lettuce_webdriver.webdriver.goto(step, world.config["django"]["base_web_url"] + "/")
        lettuce_webdriver.webdriver.fill_in_textfield(step, "username", world.config["django"]["webuser"])
        lettuce_webdriver.webdriver.fill_in_textfield(step, "password", world.config["django"]["webpassword"])
        lettuce_webdriver.webdriver.press_button(step, "Sign in")
        time.sleep(1.0)
        lettuce_webdriver.webdriver.see(step, "Service Directory - Home")

    def fill_in(self, step, field, value):
        """
        Fill in with the given value in the given field.
        :param step: current Lettuce step.
        :param field: id of the field to be filled.
        :param value: text to fill in the field.
        """
        value = self.parse_variables(value)
        lettuce_webdriver.webdriver.fill_in_textfield(step, field, value)

    def the_title_should_be(self, step, title):
        time.sleep(1.0)
        assert world.browser.title == title

    def close_browser(self, ):
        """
        Close the navigator window.
        """
        world.browser.quit()

    def parse_variables(self, template):
        """
        Build a string with the right values in the placeholders of the template
        provided.
        :param template: template to set the corresponding values.
        :return The string built
        """
        """Replace the values in the template."""
        if "$base_web_url" in template:
            base_web_url = world.config["django"]["base_web_url"]
        else:
            base_web_url = None
        if "$login_url" in template:
            login_url = world.config["django"]["login_url"]
        else:
            login_url = None
        if "$base_api_url" in template:
            base_api_url = world.config["django"]["base_api_url"]
        else:
            base_api_url = None
        if "$apis_url" in template:
            apis_url = world.config["django"]["apis_url"]
        else:
            apis_url = None
        if "$api_name" in template:
            old_api_name = world.old_capability[world.config["keys"]["api_name"]]
        else:
            old_api_name = None
        if "$endpoints_url" in template:
            endpoints_url = world.config["django"]["endpoints_url"]
        else:
            endpoints_url = None
        if "$endpoint_id" in template:
            old_endpoint = world.old_endpoint[world.config["keys"]["id"]]
        else:
            old_endpoint = None
        if "$add_cap_url" in template:
            add_cap_url = world.config["django"]["add_cap_url"]
        else:
            add_cap_url = None
        if "$capabilities_url" in template:
            capabilities_url = world.config["django"]["capabilities_url"]
        else:
            capabilities_url = None
        if "$user" in template:
            user = world.config["django"]["webuser"]
        else:
            user = None
        if "$password" in template:
            password = world.config["django"]["webpassword"]
        else:
            password = None
        if "$search_cap_url" in template:
            search_cap_url = world.config["django"]["search_cap_url"]
        else:
            search_cap_url = None
        if "$search_end_url" in template:
            search_end_url = world.config["django"]["search_end_url"]
        else:
            search_end_url = None
        if "$description" in template:
            old_description = world.old_capability[world.config["keys"]["description"]]
        else:
            old_description = None
        if "$default_version" in template:
            old_default_version = world.old_capability[world.config["keys"]["default_version"]]
        else:
            old_default_version = None
        if "$url" in template:
            old_url = world.old_endpoint[world.config["keys"]["url"]]
        else:
            old_url = None
        if "$version" in template:
            old_version = world.old_endpoint[world.config["keys"]["version"]]
        else:
            old_version = None
        if "$environment" in template:
            old_environment = world.old_endpoint[world.config["keys"]["environment"]]
        else:
            old_environment = None
        if "$ob" in template:
            old_ob = world.old_endpoint[world.config["keys"]["ob"]]
        else:
            old_ob = None
        temp = Template(template)
        template = temp.safe_substitute(base_web_url=base_web_url,
            login_url=login_url, base_api_url=base_api_url, apis_url=apis_url,
            api_name=old_api_name, endpoints_url=endpoints_url,
            endpoint_id=old_endpoint, add_cap_url=add_cap_url,
            capabilities_url=capabilities_url, user=user, password=password,
            search_cap_url=search_cap_url, search_end_url=search_end_url,
            description=old_description, default_version=old_default_version,
            url=old_url, version=old_version, environment=old_environment,
            ob=old_ob)
        return template
