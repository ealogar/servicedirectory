'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''


class SdAdminLibraryException(Exception):
    def __init__(self, message='Service Directory is not responding properly to your request. Try again later or contact Service directory support service'):
        super(SdAdminLibraryException, self).__init__(message)


class NotFoundException(SdAdminLibraryException):
    def __init__(self, id_res):
        msg = 'Resource {0} not found'.format(id_res)
        super(NotFoundException, self).__init__(msg)


class ServerException(SdAdminLibraryException):
    def __init__(self, json_details, message='Remote Exception in Service Directory'):
        if any(map(lambda x: x not in ('exceptionId', 'exceptionText'), json_details.keys())):
            raise SdAdminLibraryException('invalid exception json from SD')

        self.json_details = json_details
        super(ServerException, self).__init__(message)
