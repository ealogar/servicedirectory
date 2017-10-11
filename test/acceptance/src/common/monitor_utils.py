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
import requests
import time
import sys
from threading import Thread


class MonitorUtils(object):
    """
    Monitoring and IP in order to obtain the time during the IP isn't stable
    Implemented regarding the configuration of our front-end balancer using the Round Robin mechanism
    """

    ip = ""
    monitor_started = False
    count_stable_requests = 0
    node_stable = True
    time_unstable = {"start": 0.0, "stop": 0.0}
    thread = None

    def monitor(self, ip, timeout):
        print 'Monitoring...'
        while self.monitor_started:
            try:
                response = requests.get('http://' + ip + '/sd/v1/classes', timeout=timeout)
                if response.status_code >= 500:
                    raise requests.exceptions.Timeout
                elif self.time_unstable["start"] > 0.0:
                    if self.count_stable_requests != 5:
                        if self.count_stable_requests == 1:
                            self.time_unstable["stop"] = time.time()
                        self.count_stable_requests += 1
                    else:
                        self.node_stable = True
                        self.monitor_started = False
            except requests.exceptions.Timeout:
                if self.node_stable:
                    self.time_unstable["start"] = time.time() - timeout
                    self.node_stable = False
                    self.count_stable_requests = 0
                else:
                    self.count_stable_requests = 0
            finally:
                time.sleep(1)

    def get_time_unstabilized(self):
        print 'Waiting...',
        while self.monitor_started:
            time.sleep(2)
            print '.',
            sys.stdout.flush()
        return self.time_unstable["stop"] - self.time_unstable["start"]

    def start_monitoring(self, ip, timeout):
        self.thread = Thread(target=self.monitor, args=(ip, timeout))
        self.monitor_started = True
        self.time_unstable = {"start": 0.0, "stop": 0.0}
        self.count_stable_requests = 0
        self.thread.start()

    def stop_monitoring(self):
        self.thread.join()
        self.monitor_started = False
