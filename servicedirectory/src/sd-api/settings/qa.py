'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
from common import *

DEBUG = True

# ######## MONGO standalone configuration in QA
MONGODB = {'hosts': ('localhost:27017',),
            'dbname': 'sd',
            'slave_ok': True,
            'replicaset_number': 1,
            'replicaset': '',
            'autostart': True
            }
