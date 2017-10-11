'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''


# We subclass Exception to have semantic exceptions names inside library

class SDLibraryException(Exception):
    def __init__(self, message='Service Directory Library Exception'):
        super(SDLibraryException, self).__init__(message)


class ConnectionException(SDLibraryException):
    def __init__(self, message='Can not connect to Service Directory'):
        super(ConnectionException, self).__init__(message)


class RemoteException(SDLibraryException):
    def __init__(self, message='Remote Exception in Service Directory'):
        super(RemoteException, self).__init__(message)
