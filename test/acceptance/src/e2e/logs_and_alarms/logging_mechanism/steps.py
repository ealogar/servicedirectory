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
from common.test_utils import TestUtils
from common.rest_utils import RestUtils
from common.sd_utils import SDUtils
from common.api_utils import APIUtils
from common.mongo_utils import MongoUtils
from common.log_utils import LogUtils
import time

test_utils = TestUtils()
sd_utils = SDUtils()
rest_utils = RestUtils()
api_utils = APIUtils()
mongo_utils = MongoUtils()
log_utils = LogUtils()


@step(u'the DB is working')
def the_db_is_working(step):
    mongo_utils.the_db_is_working(step)


@step(u'the DB has stopped working')
def the_db_has_stopped_working(step):
    mongo_utils.the_db_has_stopped_working(step)


@step(u'the users DB is restored')
def the_users_DB_is_restored(step):
    mongo_utils.reset_users_database()


@step(u'the passwords have been deleted')
def the_passwords_have_been_deleted(step):
    mongo_utils.the_passwords_have_been_deleted()


@step(u'the DB has no classes already published')
def the_db_has_no_classes_already_published(step):
    pass    # the database is cleaned before each scenario


@step(u'the config file does not contain the default admin credentials')
def the_config_file_does_not_contain_the_default_admin_credentials(step):
    sd_utils.config_file_does_not_contain_default_admin_credentials()


@step(u'the config file does not contain the correlator header')
def the_config_file_does_not_contain_the_correlator_header(step):
    sd_utils.config_file_does_not_contain_the_correlator_header()


@step(u'the json schemas are missing')
def the_json_schemas_are_missing(step):
    sd_utils.json_schemas_are_missing()


@step(u'the json schemas folder is missing')
def the_json_schemas_folder_is_missing(step):
    sd_utils.json_schemas_folder_is_missing()


@step(u'a class has already been published with data:')
def a_class_has_already_been_published_with_data(step):
    api_utils.a_class_has_already_been_published_with_data(step, 0)


@step(u'I send to (.*) the data (.*)')
def i_send_to_url_the_data(step, url, data):
    rest_utils.send_to_url_the_data(step, url, data)


@step(u'I send to (.*) the class data:')
def i_send_to_url_the_class_data(step, url):
    api_utils.send_to_url_the_class_data(step, url, 0, {})


@step(u'I send to (.*) the class data with unica_correlator (.*):')
def i_send_to_url_the_class_data_with_unica_correlator(step, url, correlator):
    api_utils.send_to_url_the_class_data(step, url, 0, {"Unica-Correlator": correlator})


@step(u'I restart the Service Directory')
def i_restart_the_service_directory(step):
    sd_utils.stop_sd()
    sd_utils.start_sd()


@step(u'I request a resource (.*)')
def request_the_resource(step, url):
    rest_utils.request_the_resource(step, url)


@step(u'When I request the resource (.*) with parameters:')
def request_the_resource_with_parameters(step, url):
    rest_utils.request_the_resource(step, url, 0)


@step(u'the format of the logs is correct')
def the_format_of_the_logs_is_correct(step):
    time.sleep(1)
    log_utils.check_log_format(world.config["sd_server"]["log_path"],
                               world.config["sd_server"]["log_file"])


@step(u'I see in the logs an entry with the following data:')
def i_see_in_the_logs_an_entry_with_the_following_data(step):
    log_utils.search_in_log(world.config["sd_server"]["log_path"],
                            world.config["sd_server"]["log_file"],
                            step.hashes[0])


@step(u'I send to (.*) the instance data:')
def i_send_to_url_the_instance_data(step, url):
    api_utils.send_to_url_the_instance_data(step, url, 0)


@step(u'the user performing the operation is:')
def the_user_performing_the_operation_is(step):
    world.request_user = step.hashes[0]["username"]
    world.request_password = step.hashes[0]["password"]
    assert True


@step(u'a user has already been created with data:')
def a_user_has_already_been_created_with_data(step):
    i_send_to_url_the_user_data(step, "$base_api_url/$users_url", 0)


@step(u'I send to (.*) the user data (\d+):')
def i_send_to_url_the_user_data(step, url, user_data_index):
    api_utils.send_to_url_the_user_data(step, url, user_data_index)


@step(u'no authentication method is provided')
def no_authentication_method_is_provided(step):
    world.request_user = None
    world.request_password = None


@step(u'I try to put in (.*) the class data:')
def i_put_to_url_the_class_data(step, url):
    rest_utils.put_in_url_the_data(step, url, step.hashes[0])


@step(u'an instance has already been published with data:')
def an_instance_has_already_been_published_with_data(step):
    api_utils.an_instance_has_already_been_published_with_data(step,  0)


@step(u'the following bindings rules are available:')
def the_following_bindings_rules_are_available(step):
    api_utils.the_following_bindings_rules_are_avalilabe(step, "0")


@step(u'And the previous bindings are published for the context:')
def and_the_previous_bindings_are_published_for_the_context_operation_index(step):
    api_utils.send_to_url_the_rule_data(step, "$base_api_url/$bindings_url", 0)


@step(u'I delete (.*)')
def i_delete_url(step, url):
    rest_utils.delete_url(step, url)


@step(u'the instance published in position (\d+) has been deleted')
def the_instance_published_has_been_deleted(step, position):
    i_delete_url(step, "$base_api_url/$classes_url/$class_name/$instances_url/" + api_utils.get_instance_id(position))


@step(u'I send to (.*) the rule data:')
def i_send_to_url_the_rule_data_table(step, url):
    api_utils.send_to_url_the_rule_data(step, url, 0)


@step(u'And unica_correlator (.*) is returned in the response')
def and_unica_correlator_is_returned_in_response(step, expected_correlator):
    api_utils.validate_correlator(expected_correlator)
