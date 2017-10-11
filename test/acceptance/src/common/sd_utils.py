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
from string import Template
import subprocess
import time
from common.test_utils import TestUtils
import os
import platform
import shutil
from distutils import dir_util
import paramiko

test_utils = TestUtils()
PS = platform.system()


class SDUtils(object):

    def start_sd(self):
        """
        Start the SD if not already started and store the process in the world.
        """

        env = world.config["environment"]["name"]
        if (PS == "Windows" and env.startswith("dev")) or (PS == "Linux" and env.startswith("qa")):
            if not hasattr(world, "sd_working") or world.sd_working == False:
                run_command_temp = Template(" ".join([world.config["environment"]["python_alias"],
                                                     world.config["sd_server"]["run_command_params"]]))
                run_command = run_command_temp.safe_substitute(env=world.config["environment"]["name"])
                out = open(world.config["sd_server"]["out_file"], 'w')
                err = open(world.config["sd_server"]["err_file"], 'w')
                world.sd_process = subprocess.Popen(run_command.split(), stdout=out, stderr=err)
                time.sleep(10)
                world.sd_working = True

        elif PS == "Linux" and env.startswith("dev"):
            if not hasattr(world, "sd_working") or world.sd_working == False:
                os.system("sudo service httpd start")
                world.sd_working = True

    def restart_remote_sd(self, ip):
        """
        Start remotely the SD.
        Note: SSHKeyPath should be named "id_rsa"

        :param ip: IP address of Service Directory Server
        """

        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=world.config["ha"]["username"])
        stdout = ssh.exec_command('sudo /sbin/service httpd restart')[1]
        response = str(stdout.readlines())
        assert True if 'OK' in response else False
        ssh.close()

    def stop_sd(self):
        """
        Stop the SD if not already stopped.
        """

        env = world.config["environment"]["name"]
        if (PS == "Windows" and env.startswith("dev")) or (PS == "Linux" and env.startswith("qa")):
            if hasattr(world, "sd_working") and world.sd_working == True:
                test_utils.kill_process(world.sd_process.pid)
                time.sleep(10)
                world.sd_working = False

        elif PS == "Linux" and env.startswith("dev"):
            if hasattr(world, "sd_working") and world.sd_working == True:
                os.system("sudo service httpd stop")
                time.sleep(10)
                world.sd_working = False

    def stop_remote_sd(self, ip):
        """
        Stop remotely the SD if not already stopped.

        :param ip: IP address of Service Directory Server

        """

        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=world.config["ha"]["username"])
        stdout = ssh.exec_command('sudo /sbin/service httpd stop')[1]
        response = str(stdout.readlines())
        assert True if 'OK' in response else False
        ssh.close()

    def sd_is_working(self):
        """
        Check whether the SD is working.
        """
        if hasattr(world, "sd_working") and world.sd_working == True:
            return True
        else:
            return False

    def config_file_does_not_contain_default_admin_credentials(self):
        """
        Remove the admin credentials from the config file, backing it up first.
        """
        self.back_up_config_file()
        if PS == "Windows":
            common_config_file = world.config["sd_server"]["common_config_file_win"]
            common_config_file_backup = world.config["sd_server"]["common_config_file_backup_win"]
        else:
            common_config_file = world.config["sd_server"]["common_config_file"]
            common_config_file_backup = world.config["sd_server"]["common_config_file_backup"]
        with open(common_config_file, "w") as ccfile:
            with open(common_config_file_backup) as ccfilebackup:
                for line in ccfilebackup:
                    if not (line.startswith("SD_USERNAME") or line.startswith("SD_PASSWORD")):
                        ccfile.write(line)

    def config_file_does_not_contain_the_correlator_header(self):
        """
        Remove the correlation header from the config file, backing it up first.
        """
        self.back_up_config_file()
        if PS == "Windows":
            common_config_file = world.config["sd_server"]["common_config_file_win"]
            common_config_file_backup = world.config["sd_server"]["common_config_file_backup_win"]
        else:
            common_config_file = world.config["sd_server"]["common_config_file"]
            common_config_file_backup = world.config["sd_server"]["common_config_file_backup"]
        with open(common_config_file, "w") as ccfile:
            with open(common_config_file_backup) as ccfilebackup:
                for line in ccfilebackup:
                    if not (line.startswith("UNICA_CORRELATOR_REQUEST_HEADER")) or \
                    (line.startswith("UNICA_CORRELATOR_RESPONSE_HEADER")):
                        ccfile.write(line)

    def json_schemas_are_missing(self):

        """
        Remove the correlation header from the config file, backing it up first.
        """
        self.back_up_schema_file()
        if PS == "Windows":
            schema_file = world.config["sd_server"]["schema_file_win"]
            os.remove(schema_file)
        else:
            schema_file = world.config["sd_server"]["schema_file"]
            os.remove(schema_file)

    def json_schemas_folder_is_missing(self):

        """
        Remove the schemas folder from the systema, backing it up first.
        """
        self.back_up_schema_folder()
        if PS == "Windows":
            schema_folder = world.config["sd_server"]["schema_folder_win"]
            shutil.rmtree(schema_folder)
        else:
            schema_folder = world.config["sd_server"]["schema_folder"]
            shutil.rmtree(schema_folder)

    def back_up_config_file(self):
        """
        Back up the current common configuration file of the SD.
        """
        if PS == "Windows":
            common_config_file = world.config["sd_server"]["common_config_file_win"]
            common_config_file_backup = world.config["sd_server"]["common_config_file_backup_win"]
        else:
            common_config_file = world.config["sd_server"]["common_config_file"]
            common_config_file_backup = world.config["sd_server"]["common_config_file_backup"]
        shutil.copy2(common_config_file, common_config_file_backup)
        world.config_file_backed_up = True

    def restore_config_file(self):
        """
        Restore a previously backed up common configuration file of the SD.
        """
        if PS == "Windows":
            common_config_file = world.config["sd_server"]["common_config_file_win"]
            common_config_file_backup = world.config["sd_server"]["common_config_file_backup_win"]
        else:
            common_config_file = world.config["sd_server"]["common_config_file"]
            common_config_file_backup = world.config["sd_server"]["common_config_file_backup"]
        shutil.copy2(common_config_file_backup, common_config_file)
        world.config_file_backed_up = False

    def delete_config_file_backup(self):
        """
        Delete a previously backed up common configuration file of the SD.
        """
        if PS == "Windows":
            common_config_file_backup = world.config["sd_server"]["common_config_file_backup_win"]
        else:
            common_config_file_backup = world.config["sd_server"]["common_config_file_backup"]
        os.remove(common_config_file_backup)

    def back_up_schema_file(self):
        """
        Back up the current class schema configuration file of the SD.
        """
        if PS == "Windows":
            schema_file = world.config["sd_server"]["schema_file_win"]
            schema_file_backup = world.config["sd_server"]["schema_file_backup_win"]
        else:
            schema_file = world.config["sd_server"]["schema_file"]
            schema_file_backup = world.config["sd_server"]["schema_file_backup"]

        shutil.copy2(schema_file, schema_file_backup)
        world.schema_file_backed_up = True

    def restore_schema_file(self):
        """
        Restore a previously backed up common configuration file of the SD.
        """
        if PS == "Windows":
            schema_file = world.config["sd_server"]["schema_file_win"]
            schema_file_backup = world.config["sd_server"]["schema_file_backup_win"]
        else:
            schema_file = world.config["sd_server"]["schema_file"]
            schema_file_backup = world.config["sd_server"]["schema_file_backup"]
        shutil.copy2(schema_file_backup, schema_file)
        world.schema_file_backed_up = False

    def delete_schema_file_backup(self):
        """
        Delete a previously backed up common configuration file of the SD.
        """
        if PS == "Windows":
            schema_file_backup = world.config["sd_server"]["schema_file_backup_win"]
        else:
            schema_file_backup = world.config["sd_server"]["schema_file_backup"]

        os.remove(schema_file_backup)

    def back_up_schema_folder(self):
        """
        Back up the current schemas folder of the SD.
        """
        if PS == "Windows":
            schema_folder = world.config["sd_server"]["schema_folder_win"]
            schema_folder_backup = world.config["sd_server"]["schema_folder_backup_win"]
        else:
            schema_folder = world.config["sd_server"]["schema_folder"]
            schema_folder_backup = world.config["sd_server"]["schema_folder_backup"]
        dir_util.copy_tree(schema_folder, schema_folder_backup)
        world.schema_folder_backed_up = True

    def restore_schema_folder(self):
        """
        Restore a previously backed up common configuration file of the SD.
        """
        if PS == "Windows":
            schema_folder = world.config["sd_server"]["schema_folder_win"]
            schema_folder_backup = world.config["sd_server"]["schema_folder_backup_win"]
        else:
            schema_folder = world.config["sd_server"]["schema_folder"]
            schema_folder_backup = world.config["sd_server"]["schema_folder_backup"]
        dir_util.copy_tree(schema_folder_backup, schema_folder)
        world.schema_folder_backed_up = False

    def delete_schema_folder_backup(self):
        """
        Delete a previously backed up common configuration file of the SD.
        """
        if PS == "Windows":
            schema_folder_backup = world.config["sd_server"]["schema_folder_backup_win"]
        else:
            schema_folder_backup = world.config["sd_server"]["schema_folder_backup"]
        shutil.rmtree(schema_folder_backup)
