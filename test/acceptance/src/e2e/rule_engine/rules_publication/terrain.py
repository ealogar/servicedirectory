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
from lettuce import before, after, world
from common.test_utils import TestUtils
from common.mongo_utils import MongoUtils
from common.sd_utils import SDUtils
from common.api_utils import APIUtils

test_utils = TestUtils()
mongo_utils = MongoUtils()
sd_utils = SDUtils()
api_utils = APIUtils()


@before.all
def before_all():
    test_utils.initialize()


@after.all
def after_all(total):
    if world.config["environment"]["run_test"] in "local":
        mongo_utils.reset_mongo()
        sd_utils.stop_sd()
    if world.config["environment"]["run_test"] in "remote":
        api_utils.reset_SD()


@before.each_scenario
def before_each_scenario(scenario):

    if world.config["environment"]["run_test"] in "local":
        sd_utils.start_sd()
        mongo_utils.reset_mongo()
    if world.config["environment"]["run_test"] in "remote":
        api_utils.reset_SD()
