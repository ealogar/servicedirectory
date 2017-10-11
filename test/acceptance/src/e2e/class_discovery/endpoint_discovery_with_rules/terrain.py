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
from lettuce import before, after
from common.test_utils import TestUtils
from common.mongo_utils import MongoUtils
from common.sd_utils import SDUtils

test_utils = TestUtils()
mongo_utils = MongoUtils()
sd_utils = SDUtils()


@before.all
def before_all():

    test_utils.initialize()


@after.all
def after_all(total):

    mongo_utils.reset_mongo()
    sd_utils.stop_sd()


@before.each_scenario
def before_each_scenario(scenario):

    sd_utils.start_sd()
    mongo_utils.reset_mongo()
