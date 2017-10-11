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
from common.cli_utils import CLIUtils
from component.common.mock_utils import SDMockUtils


mongo_utils = MongoUtils()
cli_utils = CLIUtils()
mock_utils = SDMockUtils()


@step(u'the CLI is installed and ready to be executed')
def the_CLI_is_installed_and_ready_to_be_executed(step):
    cli_utils.back_up_config_file()
    cli_utils.start_cli()


@step(u'the SD is ready to return the version info:')
def the_SD_is_i_ready_to_return_the_version_info(step):
    mock_utils.get_request_and_send_response_of_type_with_data(step, "sd/info", 200, 0)


@step(u'the SD is ready to return the class:')
def the_SD_is_i_ready_to_return_the_class(step):
    mock_utils.get_request_and_send_response_of_type_with_data(step, "sd/v1/classes", 200, 0)


@step(u'the CLI is configured with the configuration (\d+):')
def the_CLI_is_configured_with_the_configuration(step, cliconfig_index):
    cli_utils.the_CLI_is_configured_with_the_configuration(step, cliconfig_index)


@step(u'I request the info')
def I_request_the_info(step):
    cli_utils.send_cli("info")


@step(u'I request the operation (\d+):')
def I_request_the_operation(step, operation_index):
    cli_utils.send_cli(step.hashes[int(operation_index)]["operation"] +\
                        " " + step.hashes[int(operation_index)]["arguments"])


@step(u'the result set contains the data (\d+):')
def the_result_set_contains_the_data(step, data_index):
    cli_utils.validate_data(step, data_index)


@step(u'the configuration contains the data (\d+):')
def the_configuration_contains_the_data(step, data_index):
    cli_utils.validate_configuration(step, data_index)


@step(u'the error contains the data (.*):')
def the_error_contains_the_data(step, data_index):
    cli_utils.validate_error(step, data_index)


@step(u'the CLI config file has been removed')
def the_CLI_config_file_has_been_removed(step):
    cli_utils.delete_cli_config()


@step(u'the CLI config file has been substituted')
def the_CLI_config_file_has_been_substituted(step):
    cli_utils.change_cli_config()


@step(u'the CLI config file has lost the property (\d+):')
def the_CLI_config_file_has_lost_the_property(step, property_index):
    cli_utils.erase_property(step.hashes[int(property_index)]["property"])


@step(u'the config file is restored')
def the_config_file_is_restored(step):
    cli_utils.restore_config_file()


@step(u'the config file is stored')
def the_config_file_is_stored(step):
    cli_utils.back_up_config_file()
