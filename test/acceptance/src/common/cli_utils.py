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
from lettuce import world
import subprocess
from common.test_utils import TestUtils
from common.sd_utils import SDUtils
import os
import platform
import shutil
import re
import json


sd_utils = SDUtils()
test_utils = TestUtils()
CLI_execute = "sd-cli "
PS = platform.system()


class CLIUtils(object):

    def start_cli(self):

        my_env = os.environ
        my_env['PYTHONIOENCODING'] = 'utf-8'
        world.CLI = subprocess.Popen("cmd.exe /k",  stdout=subprocess.PIPE,
          stderr=subprocess.PIPE, stdin=subprocess.PIPE, env=my_env)

    def send_cli(self, command):

        world.CLI_command = command
        world.CLI_response = world.CLI.communicate(("".join([CLI_execute, command + "\r\n"])).encode("utf-8"))
        #print "CLI response: ", world.CLI_response

    def validate_data(self, step, data_index):

        message = step.hashes[int(data_index)]["message"]
        data = step.hashes[int(data_index)]
        operation = step.hashes[int(data_index)]["operation_type"] + " " + step.hashes[int(data_index)]["operator"]

        commands_list = world.CLI_response[0].split("\r\n\r\n")

        result = (commands_list[0].split(("".join([CLI_execute, world.CLI_command + "\r\n"])).encode("utf-8")))[1]

        if  "[EMPTY]" not in data["operation_type"]:
            assert  operation == result.splitlines()[0], "Operation type not found in response. \
            Expected %s, received %s" % (operation, result.splitlines()[0])

            try:
                """Remove the operation type from data to compare results"""
                sanitized_result = eval(result.replace(operation, ""))[0]
            except:
                """No extra content"""
                sanitized_result = ""

        else:
            try:
                sanitized_result = eval(result)
            except:
                """Can not apply eval to simple text"""
                sanitized_result = result

        """ Remove contend added by CLI leaving in the step the content expected from SD """
        del data["operation_type"]
        del data["operator"]
        del data["message"]

        """ Validate additional data just in case it is expected in the step """
        if len(data) != 0:

            assert len(data) == len(sanitized_result), "Unexpected response received. Expected: %s. Received: %s." \
            % (len(data), len(sanitized_result))
            for item in sanitized_result:
                if item in data:
                    pass
                else:
                    assert False, "Received value not expected ins response. Value: %s. Expected response: %s." \
                    % (item, data)

        elif "[EMPTY]" not in message:
            """ Simple message. Validate text """
            assert message == result, "Received message is not the expected message. Expected: %s. Received: %s." \
            % (message, result)

    def validate_collection(self, step):

        commands_list = world.CLI_response[0].split("\r\n\r\n")
        result = (commands_list[0].split("".join([CLI_execute, world.CLI_command + "\r\n"])))[1]

        for item in step.hashes:
                """ Format the step values when they contain json values """
                """ If attributes in expected body, transform them into json """
                try:
                    item["attributes"] = json.loads(item["attributes"])
                except:
                    pass
                """ If binding tules in expected body, transform them into json """
                try:
                    item["binding_rules"] = json.loads(item["binding_rules"])
                except:
                    pass

        assert step.hashes == eval(result), "The result received is not the result expected. \
        Expected %s, received %s" % (step, step)

    def validate_item(self, step, data_index):

        commands_list = world.CLI_response[0].split("\r\n\r\n")
        result = (commands_list[0].split("".join([CLI_execute, world.CLI_command + "\r\n"])))[1]

        """ Format the step values when they contain json values """
        """ If attributes in expected body, transform them into json """
        try:
            step.hashes[int(data_index)]["attributes"] = json.loads(step.hashes[int(data_index)]["attributes"])
        except:
            pass
        """ If binding tules in expected body, transform them into json """
        try:
            step.hashes[int(data_index)]["binding_rules"] = json.loads(step.hashes[int(data_index)]["binding_rules"])
        except:
            pass

        assert step.hashes[int(data_index)] == eval(result), "The result received is not the result expected. \
        Expected %s, received %s" % (step.hashes[int(data_index)], eval(result))

    def validate_help(self, step):

        result = world.CLI_response
        assert "Usage" in result[1], "Help usage has not been launched"

    def validate_configuration(self, step, data_index):

        result = world.CLI_response[0].splitlines()

        for parameter in step.hashes[int(data_index)]:
            located_param = False
            for line in result:
                if "[FILE]" not in step.hashes[int(data_index)][parameter]:
                    if  line.startswith(parameter + "=" + step.hashes[int(data_index)][parameter]) or line.startswith("#" + parameter + "=" + step.hashes[int(data_index)][parameter]):
                        located_param = True
                else:
                    if  line.startswith(parameter) or line.startswith("#"+parameter):
                        located_param = True
            assert located_param, "Error validating the configuration parameter %s" % parameter

    def validate_error(self, step, error_index):

        commands_list = world.CLI_response[0].split("\r\n\r\n")
        result = ((commands_list[0].split("".join([CLI_execute, world.CLI_command + "\r\n"])))[1])

        if error_index == "all":
            index = 0
            for item in step.hashes:
                    assert re.search(item["message"] ,result.splitlines()[index]), "Error type not found in response. \
                    Expected %s, received %s" % (item["message"], result.splitlines()[index])
                    index = index + 1
        else:
            assert step.hashes[int(error_index)]["error_type"] == result.splitlines()[0], "Error type not found in response. \
                Expected %s, received %s" % (step.hashes[int(error_index)]["error_type"], result.splitlines()[0])

            if "[SD Error]:" in step.hashes[int(error_index)]["error_type"]:
                assert "code: " + step.hashes[int(error_index)]["exceptionId"] == result.splitlines()[1], \
                "exceptionId not found in response. Expected %s, received %s" % (step.hashes[int(error_index)]["exceptionId"], result.splitlines()[1])
                assert "message: " + step.hashes[int(error_index)]["exceptionText"] == result.splitlines()[2], \
                "ExceptionText not found in response. Expected %s, received %s" \
                % (step.hashes[int(error_index)]["exceptionText"], result.splitlines()[2])

            if "[CLI Error]:" in   step.hashes[int(error_index)]["error_type"]:
                assert re.search(step.hashes[int(error_index)]["message"],  result), "Error message not found in response. \
                Expected %s, received %s" % (step.hashes[int(error_index)]["message"], result)

    def delete_cli_config(self):

        """
        Remove the admin file.
        """
        self.back_up_config_file()
        if PS == "Windows":
            common_config_file = world.config["cli_client"]["common_config_file_win"]
        else:
            common_config_file = world.config["cli_client"]["common_config_file"]

        os.remove(common_config_file)

    def change_cli_config(self):

        """
        Change the admin file.
        """
        self.back_up_config_file()
        if PS == "Windows":
            common_config_file = world.config["cli_client"]["common_config_file_win"]
        else:
            common_config_file = world.config["cli_client"]["common_config_file"]

        shutil.copy2( "./component/cli/cli_configuration/bad_cli.conf",common_config_file)

    def erase_property(self, key):
        """
        Remove a property from configuration file.
        """
        self.back_up_config_file()
        if PS == "Windows":
            common_config_file = world.config["cli_client"]["common_config_file_win"]
            common_config_file_backup = world.config["cli_client"]["common_config_file_backup_win"]
        else:
            common_config_file = world.config["cli_client"]["common_config_file"]
            common_config_file_backup = world.config["cli_client"]["common_config_file_backup"]
        with open(common_config_file, "w") as ccfile:
            with open(common_config_file_backup) as ccfilebackup:
                for line in ccfilebackup:
                    if not (line.startswith(key)):
                        ccfile.write(line)

    def the_CLI_is_configured_with_the_configuration(self, step, cliconfig_index):
        """
        Configure the configuration file with values.
        """
        """ Store the sd-cli -s output with the original config file for future validations"""
        """ TBD"""
        for config_param in step.hashes[int(cliconfig_index)].keys():
            if not "[FILE]" in step.hashes[int(cliconfig_index)][config_param]:
                self.write_property(config_param, step.hashes[int(cliconfig_index)][config_param])

    def write_property(self, conf_property_key, conf_property_value):
        """
        Configure a conf_property in the configuration file.
        """
        if PS == "Windows":
            common_config_file = world.config["cli_client"]["common_config_file_win"]
            common_config_file_backup = world.config["cli_client"]["common_config_file_backup_win"]
        else:
            common_config_file = world.config["cli_client"]["common_config_file"]
            common_config_file_backup = world.config["cli_client"]["common_config_file_backup"]
        with open(common_config_file, "w") as ccfile:
            with open(common_config_file_backup) as ccfilebackup:
                for line in ccfilebackup:
                    if (line.startswith(conf_property_key)) or (line.startswith("#"+conf_property_key)) :
                        ccfile.write(conf_property_key + "=" + conf_property_value + "\r\n")
                    else:
                        ccfile.write(line)

    def back_up_config_file(self):
        """
        Back up the current common configuration file of the CLI.
        """
        if PS == "Windows":
            common_config_file = world.config["cli_client"]["common_config_file_win"]
            common_config_file_backup = world.config["cli_client"]["common_config_file_backup_win"]
        else:
            common_config_file = world.config["cli_client"]["common_config_file"]
            common_config_file_backup = world.config["cli_client"]["common_config_file_backup"]
        shutil.copy2(common_config_file, common_config_file_backup)
        world.config_file_backed_up = True

    def restore_config_file(self):
        """
        Restore a previously backed up common configuration file of the SD.
        """
        if PS == "Windows":
            common_config_file = world.config["cli_client"]["common_config_file_win"]
            common_config_file_backup = world.config["cli_client"]["common_config_file_backup_win"]
        else:
            common_config_file = world.config["cli_client"]["common_config_file"]
            common_config_file_backup = world.config["scli_client"]["common_config_file_backup"]
        shutil.copy2(common_config_file_backup, common_config_file)
        world.config_file_backed_up = False
