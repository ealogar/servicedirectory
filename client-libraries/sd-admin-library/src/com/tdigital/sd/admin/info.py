'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''


class Info(object):
    """Service Directory info

    This class provides access to the gateway info report
    """

    PATH_INFO = '../info'

    def __init__(self, client):
        """Constructor

        Stores a HTTP client reference to access the service directory

        :param client HTTP client to access service directory (Mandatory)
                      It is an instance of com.tdigital.sd.admin.client.Client class
        """

        self.client = client

    def info(self):
        """Get service directory info

        Get the default version and other details provided by the service directory
        """

        return self.client.get(Info.PATH_INFO)
