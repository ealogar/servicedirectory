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
import json
import psutil
import os
import sqlite3
import subprocess


class TestUtils(object):

    def initialize(self):
        """
        Parse the JSON configuration file located in the execution folder and
        store the resulting dictionary in the world.
        """
        with open("properties.json") as config_file:
            world.config = json.load(config_file)

        """
        Make sure the logs path exists and create it otherwise.
        """
        if not os.path.exists(world.config["environment"]["logs_path"]):
            os.makedirs(world.config["environment"]["logs_path"])
        """
        Set up db auth users if needed.
        """
        if (self._is_db_sync() == False):
            FNULL = open(os.devnull, 'w')
            subprocess.call(["python", "../../src/web-admin-sd/sd-web/manage.py", "syncdb", "--noinput"],\
                             stdout=FNULL, stderr=FNULL)
            subprocess.call(["python", "../../src/web-admin-sd/sd-web/manage.py", "loaddata", "initial_data.json"],\
                             stdout=FNULL, stderr=FNULL)

        """
        Clean world variables.
        """
        self.reset_world()

    def reset_world(self):
        """
        Clean world variables.
        """
        world.bindings = []
        world.binding_rules = []
        world.endpoints_history = []
        world.instances_history = []
        world.bindings_history = []

        """
        Request set values.
        """
        world.request_user = None
        world.request_password = None

    def kill_process(self, pid):
        """
        It kills all children processes and the process with the pid given.
        :param pid the pid of the process to kill
        """
        parent = psutil.Process(pid)
        for child in parent.get_children(recursive=True):
            child.kill()
        parent.kill()

    def _is_db_sync(self):
        """
        Check wether Service Directory sqlite3 db is synced or not.
        """
        res = False
        try:
            sqlite3.connect()
            conn = sqlite3.connect('../../src/web-admin-sd/sd-web/sd.db')
            c = conn.cursor()
            for row in c.execute('SELECT username FROM auth_user'):
                if row[0] == 'admin':
                    res = True
                    break
        except:
            print "Sqlite3 not initialized"
        return res
