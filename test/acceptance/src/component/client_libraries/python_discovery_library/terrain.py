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
from component.common.mock_utils import SDMockUtils
from common.test_utils import TestUtils

test_utils = TestUtils()
sd_mock_utils = SDMockUtils()


@before.all
def before_all():
    test_utils.initialize()


@after.all
def after_all(total):
    sd_mock_utils.stop_sd_mock()


@before.each_scenario
def before_each_scenario(scenario):
    sd_mock_utils.start_sd_mock()
