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
import time

test_utils = TestUtils()
mongo_utils = MongoUtils()
sd_utils = SDUtils()
api_utils = APIUtils()


@before.all
def before_all():
    test_utils.initialize()
    mongo_utils.lookup_ha_network()


@after.all
def after_all(total):
    restart_all()


def restart_all():
    for ip in world.config["ha"]["mongo_list"]:
        print 'Restart MongoDB: ', ip
        mongo_utils.restart_remote_mongo(str(ip))
    for ip in world.config["ha"]["frontend_list"]:
        print 'Restart Frontend: ', ip
        sd_utils.restart_remote_sd(str(ip))

    print 'Reset SD'
    time.sleep(10)
    api_utils.reset_SD()


@before.each_scenario
def before_each_scenario(scenario):
    restart_all()
