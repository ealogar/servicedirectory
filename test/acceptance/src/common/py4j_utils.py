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
import py4j.java_gateway
import subprocess
import time


class PythonLibUtils(object):

    def start_jvm_gateway(self):
        """
        Start the JVM, connect to the JVM and store the gateway in the world.
        """
        world.jvm_gw_process = \
            subprocess.Popen(["java", "-jar", "acceptance/common/lib/py4j-entry-point.jar"])
        world.jvm_gw = py4j.java_gateway.JavaGateway(auto_convert=True)
        time.sleep(0.5)

    def stop_jvm_gateway(self):
        """
        Shuts down the gateway to stop the Java process execution.
        """
        world.jvm_gw.shutdown()
