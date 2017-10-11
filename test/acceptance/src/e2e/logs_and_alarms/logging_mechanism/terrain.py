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
from common.log_utils import LogUtils

test_utils = TestUtils()
mongo_utils = MongoUtils()
sd_utils = SDUtils()
log_utils = LogUtils()


@before.all
def before_all():
    test_utils.initialize()
    log_utils.reset_logs(world.config["sd_server"]["log_path"],
                         [world.config["sd_server"]["log_file"]])


@after.all
def after_all(total):
    mongo_utils.reset_users_database()
    mongo_utils.reset_mongo()
    sd_utils.stop_sd()


@before.each_scenario
def before_each_scenario(scenario):

    sd_utils.start_sd()
    mongo_utils.reset_mongo()


@after.each_scenario
def after_each_scenario(scenario):
    if hasattr(world, "config_file_backed_up") and world.config_file_backed_up == True:
        """ If the config file was overwritten in the scenario, restore it and restart. """
        sd_utils.restore_config_file()
        sd_utils.delete_config_file_backup()
        sd_utils.stop_sd()
        sd_utils.start_sd()
    if hasattr(world, "schema_file_backed_up") and world.schema_file_backed_up == True:
        """ If the schema file was overwritten in the scenario, restore it and restart. """
        sd_utils.restore_schema_file()
        sd_utils.delete_schema_file_backup()
        sd_utils.stop_sd()
        sd_utils.start_sd()

    if hasattr(world, "schema_folder_backed_up") and world.schema_folder_backed_up == True:
        """ If the schema folder was overwritten in the scenario, restore it and restart. """
        sd_utils.restore_schema_folder()
        sd_utils.delete_schema_folder_backup()
        sd_utils.stop_sd()
        sd_utils.start_sd()
