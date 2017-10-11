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
import pymongo
import platform
import subprocess
import os
import time
import re
import paramiko


class MongoUtils(object):

    def lookup_ha_network(self):
        print 'Mapping Replicaset Internal-Public IPs...'
        world.mongo_replicaset = {}
        world.mongo_replicaset_inv = {}
        for ip in world.config["ha"]["mongo_list"]:
            ssh = paramiko.SSHClient()
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, username=world.config["ha"]["username"])
            stdout = ssh.exec_command('curl 169.254.169.254/latest/meta-data/local-ipv4')[1]
            internal_ip = stdout.readlines()[0]
            world.mongo_replicaset[internal_ip] = ip
            world.mongo_replicaset_inv[ip] = internal_ip
            print internal_ip, " = ", ip
            ssh.close()

    def the_db_is_working(self, step):
        """
        Check through asserts that the DB is working.
        :param step: Current Lettuce step.
        """
        if self.mongo_is_up():
            assert True
        else:
            assert False, "Mongo DB connection failed"

    def the_db_has_stopped_working(self, step):
        """
        Make the DB stop and check through asserts that it is no longer working.
        :param step: Current Lettuce step.
        """
        self.stop_mongo()
        if self.mongo_is_up():
            assert False, "The Mongo DB is not down"
        else:
            assert True

    def the_passwords_have_been_deleted(self):
        if not self.mongo_is_up():
            self.start_mongo()
        host = world.config["mongodb"]["host"]
        port = world.config["mongodb"]["port"]
        world.client = pymongo.MongoClient(host, port)
        world.db = world.client[world.config["mongodb"]["database"]]
        world.users_col = world.db[world.config["mongodb"]["users_col"]]
        world.users_col.update({}, {"$unset": {'password': True}})

    def the_db_has_been_deleted(self):
        if not self.mongo_is_up():
            self.start_mongo()
        host = world.config["mongodb"]["host"]
        port = world.config["mongodb"]["port"]
        world.client = pymongo.MongoClient(host, port)
        world.db = world.client[world.config["mongodb"]["database"]]
        world.client.drop_database(world.config["mongodb"]["database"])

    def reset_users_database(self):

        if not self.mongo_is_up():
            self.start_mongo()

        world.users_col = world.db[world.config["mongodb"]["users_col"]]
        world.users_col.remove()

    def reset_mongo(self):
        """
        Make sure the Mongo DB is working, starting it if not, and clear the data
        of the database and the collections used by the SD (but not their indexes).
        """

        #print "MONGO: Local clean-up"

        if not self.mongo_is_up():
            self.start_mongo()
        host = world.config["mongodb"]["host"]
        port = world.config["mongodb"]["port"]
        world.client = pymongo.MongoClient(host, port)
        world.db = world.client[world.config["mongodb"]["database"]]
        world.apis_col = world.db[world.config["mongodb"]["apis_col"]]
        world.apis_col.remove()
        world.endpoints_col = world.db[world.config["mongodb"]["endpoints_col"]]
        world.endpoints_col.remove()
        world.bindings_col = world.db[world.config["mongodb"]["bindings_col"]]
        world.bindings_col.remove()
        world.users_col = world.db[world.config["mongodb"]["users_col"]]
        world.users_col.remove({"_id": {"$not": re.compile("admin")}})
        world.users_col.remove({"_id": "other_admin"})

    def start_mongo(self):
        """
        Start the Mongo DB service in the appropriate way depending on the
        environment and the operating system where the DB is running.
        """
        env = world.config["environment"]["name"]
        if platform.system() == "Windows" and env.startswith("dev"):
            FNULL = open(os.devnull, 'w')
            subprocess.call("net start MongoDB", stdout=FNULL, stderr=FNULL)

        elif platform.system() == "Linux":
            os.system("sudo service mongod start")
            time.sleep(10)

    def start_remote_mongo(self, ip):
        """
        Start the Mongo DB service in the appropriate way depending on the
        environment and the operating system where the DB is running.
        """

        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=world.config["ha"]["username"])
        stdout = ssh.exec_command('sudo /sbin/service mongod restart')[1]
        response = str(stdout.readlines())
        assert True if 'OK' in response else False
        ssh.close()

    def stop_mongo(self):
        """
        Stop the Mongo DB service in the appropriate way depending on the
        environment and the operating system where the DB is running.
        """
        env = world.config["environment"]["name"]
        if platform.system() == "Windows" and env.startswith("dev"):
            FNULL = open(os.devnull, 'w')
            subprocess.call("net stop MongoDB", stdout=FNULL, stderr=FNULL)

        elif platform.system() == "Linux":
            os.system("sudo service mongod stop")
            time.sleep(10)

    def stop_remote_mongo(self, ip):
        """
        Stop the Mongo DB service in the appropriate way depending on the
        environment and the operating system where the DB is running.
        """

        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=world.config["ha"]["username"])
        stdout = ssh.exec_command('sudo /sbin/service mongod stop')[1]
        response = str(stdout.readlines())
        assert True if 'OK' in response else False
        ssh.close()

    def restart_remote_mongo(self, ip):
        """
        Restart the Mongo DB service in the appropriate way depending on the
        environment and the operating system where the DB is running.
        """

        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=world.config["ha"]["username"])
        stdout = ssh.exec_command('sudo /sbin/service mongod restart')[1]
        response = str(stdout.readlines())
        assert True if 'OK' in response else False
        ssh.close()

    def get_ip_primary_mongo(self):
        """
        Return the IP Address of the primary MongoDB
        """

        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ip = ""
        format_ok = False
        while not format_ok:
            for mongo in world.config["ha"]["mongo_list"]:
                try:
                    print 'Request for Primary to MongoDB: ', mongo
                    ssh.connect(mongo, username=world.config["ha"]["username"])
                    stdout = ssh.exec_command("mongo --eval 'db.isMaster()[\"primary\"]'")[1]
                    output = stdout.readlines()
                    print 'Response: ', output
                    ip = output[2].split(':')[0]
                    print 'Check Primary IP: ', ip
                    format_ok = re.compile("(\d+).(\d+).(\d+).(\d+)").match(ip)
                    if format_ok:
                        break
                except:
                    time.sleep(5)

        public_ip = world.mongo_replicaset[ip]
        world.primary_mongo = public_ip
        ssh.close()
        return public_ip

    def is_primary_mongodb(self, ip):
        return ip == self.get_ip_primary_mongo()

    def mongo_is_up(self):
        """
        Check if the Mongo DB service is working by connecting to the DB.
        """
        host = world.config["mongodb"]["host"]
        port = world.config["mongodb"]["port"]
        try:
            pymongo.Connection(host, port)
            return True
        except:
            return False

    def get_mongo_version(self):
        """
        Get the mongo version from the local mongo db instance.
        """
        host = world.config["mongodb"]["host"]
        port = world.config["mongodb"]["port"]
        return pymongo.Connection(host, port).server_info()["version"]
