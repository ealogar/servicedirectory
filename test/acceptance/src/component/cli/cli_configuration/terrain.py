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
from common.cli_utils import CLIUtils
from component.common.mock_utils import SDMockUtils

test_utils = TestUtils()
mongo_utils = MongoUtils()
sd_utils = SDUtils()
cli_utils = CLIUtils()
sd_mock_utils = SDMockUtils()


@before.all
def before_all():
    test_utils.initialize()


@after.all
def after_all(total):
    sd_mock_utils.stop_sd_mock()
    if hasattr(world, "config_file_backed_up") and world.config_file_backed_up == True:
        """ If the config file was overwritten in the scenario, restore it and restart. """
        cli_utils.restore_config_file()


@before.each_scenario
def before_each_scenario(scenario):
    sd_mock_utils.start_sd_mock()
    if hasattr(world, "config_file_backed_up") and world.config_file_backed_up == True:
        """ If the config file was overwritten in the scenario, restore it and restart. """
        cli_utils.restore_config_file()
