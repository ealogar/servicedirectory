'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''


class NotFoundException(Exception):
    """
    Add details to represent error message for all exceptions.
    Subclasses will have details message and all parames needed
    for exception_mapper.
    """
    def __init__(self, details=None):
        self._details = details

    def __str__(self):
        return repr(self._details)
