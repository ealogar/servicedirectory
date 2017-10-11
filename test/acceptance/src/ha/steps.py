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
from common.sd_utils import SDUtils
from common.mongo_utils import MongoUtils
from common.monitor_utils import MonitorUtils

rest_utils = RestUtils()
test_utils = TestUtils()
api_utils = APIUtils()
mongo_utils = MongoUtils()
sd_utils = SDUtils()
monitor_utils = MonitorUtils()


@step(u'the user performing the operation is:')
def the_user_performing_the_operation_is(step):
    test_utils.reset_world()
    world.request_user = step.hashes[0]["username"]
    world.request_password = step.hashes[0]["password"]
    assert True


@step(u'a class has already been published with data (\d+):')
def a_class_has_already_been_published_with_data(step, old_class_index):
    api_utils.a_class_has_already_been_published_with_data(step, old_class_index)


@step(u'I send to (.*) the instance data (\d+):')
def i_send_to_url_the_instance_data(step, url, class_index):
    api_utils.send_to_url_the_instance_data(step, url, class_index)


@step(u'I get a success response of type (\d+) with location (.+):')
def i_get_a_success_response_of_type_with_location(step, status_code, location_index):
    rest_utils.get_a_success_response_of_type_with_location(step, status_code, location_index)


@step(u'the response contains the instance data')
def the_response_contains_the_instance_data(step):
    api_utils.the_response_contains_the_instance_data()


@step(u'the location returns the instance data')
def the_location_returns_the_instance_data(step):
    api_utils.the_url_returns_the_instance_data(step, world.location)


@step(u'wait while the content is replicated')
def wait_while_the_content_is_replicated(step):
    import time
    time.sleep(5)


@step(u'wait while the replicaset know this change')
def wait_while_the_replicaset_know_this_change(step):
    import time
    time.sleep(30)


@step(u'I request the resource (.*)')
def request_the_resource(step, url):
    rest_utils.request_the_resource(step, url)


@step(u'I get a success response of type (\d+) with a result set of size (\d+)')
def get_a_success_response_of_type_with_resultset_of_size(step, status_code, size):
    rest_utils.get_a_success_response_of_type_with_resultset_of_size(step, status_code, size)


@step(u'the frontend (\d+) has stopped working')
def the_frontend_has_stopped_working(step, frontend_index):
    world.frontend_tested = world.config["ha"]["frontend_list"][int(frontend_index)]
    sd_utils.stop_remote_sd(world.frontend_tested)


@step(u'the frontend (\d+) is working')
def the_frontend_is_working(step, frontend_index):
    world.frontend_tested = world.config["ha"]["frontend_list"][int(frontend_index)]
    sd_utils.restart_remote_sd(world.frontend_tested)


@step(u'the primary MongoDB has stopped working')
def the_primary_MongoDB_has_stopped_working(step):
    world.mongodb_tested = mongo_utils.get_ip_primary_mongo()
    mongo_utils.stop_remote_mongo(world.mongodb_tested)


@step(u'another MongoDB has stopped working')
def another_MongoDB_has_stopped_working(step):
    mongo_list = world.mongo_replicaset_inv.copy()
    mongo_list.pop(str(world.mongodb_tested))
    world.mongodb_tested = mongo_list.keys()[0]
    mongo_utils.stop_remote_mongo(world.mongodb_tested)


@step(u'the mongodb tested is restarted')
def the_mongodb_tested_is_restarted(step):
    mongo_utils.restart_remote_mongo(world.mongodb_tested)


@step(u'all MongoDB has stopped working')
def all_mongodbs_has_stoppped_working(step):
    for ip in world.config["ha"]["mongo_list"]:
        mongo_utils.stop_remote_mongo(str(ip))


@step(u'all MongoDB are working')
def all_mongodbs_has_working(step):
    for ip in world.config["ha"]["mongo_list"]:
        mongo_utils.start_remote_mongo(str(ip))


@step(u'the MongoDB tested is working')
def the_MongoDB_tested_is_working(step):
    mongo_utils.start_remote_mongo(world.mongodb_tested)


@step(u'the mongodb tested is the primary MongoDB')
def the_mongodb_tested_is_the_primary_mongodb(step):
    assert mongo_utils.is_primary_mongodb(world.mongodb_tested)


@step(u'I get an error response of type (\d+) with error code (\w+)')
def i_get_an_error_response_of_type_with_error_code(step, status_type, error_code):
    rest_utils.get_an_error_response_of_type_with_error_code(step, status_type, error_code)


@step(u'monitoring (\w+) while request timeout more than (\d+) milliseconds')
def start_monitoring_ip_while_request_timeout_more_than(steps, ip, timeout):
    try:
        if 'balancer' in ip:
            ip = world.config["ha"]["frontend_balancer"]
        monitor_utils.start_monitoring(ip, float(timeout) / 1000)
    except Exception, err:
        print err


@step(u'wait while monitoring is not stabilized')
def wait_while_monitoring_is_not_stabilized(step):
    world.time_unstabilized = monitor_utils.get_time_unstabilized()
    print 'Time unstable(s): ', world.time_unstabilized
    print


@step(u'stop monitoring (\w+)')
def stop_monitoring_ip(steps, ip):
    try:
        if 'balancer' in ip:
            ip = world.config["ha"]["frontend_balancer"]
        monitor_utils.stop_monitoring()
    except Exception, err:
        print err


@step(u'time unstable is less than (\d+) seconds')
def time_unstable_is_less_than_x_seconds(steps, seconds):
    print float(world.time_unstabilized), ' <= ', float(seconds)
    assert float(world.time_unstabilized) <= float(seconds)


@step(u'the frontend (.*) is not a valid IP for balancer')
def the_frontend_is_not_a_valid_ip_for_balancer(step, frontend_index):
    #FUTURE WORK
    pass


@step(u'the time to recover the frontend is less than (\d+) seconds')
def the_time_to_recover_the_frontend_is_less_than_x_seconds(step, time):
    #FUTURE WORK
    pass


@step(u'the time to recover the mongodb is less than (\d+) seconds')
def the_time_to_recover_the_mongodb_is_less_than_x_seconds(step, time):
    #FUTURE WORK
    pass
