'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
from __future__ import unicode_literals  # Make all strings in file converted to unicode
from commons.exception_mapper.errors.errors import ERRORS


class ServiceDirectoryException(Exception):
    """
    Add details to represent error message for all exceptions.
    Subclasses will have details message and all parames needed
    for exception_mapper.
    """
    def __init__(self, details):
        if not hasattr(self, '_unica_code'):
            raise NotImplementedError("{0}._unica_code attribute must be defined when overriding"\
                                      .format(self.__class__.__name__))
        self._details = details

    def __str__(self):
        return repr(self._details)

    @property
    def unica_msg(self):
        return ERRORS[self._unica_code]['details']

    @property
    def details(self):
        return self._details

    @property
    def status_code(self):
        return int(ERRORS[self._unica_code]['status_code'])  # status_code must be integer

    @property
    def code(self):
        return self._unica_code


class GenericServiceError(ServiceDirectoryException):
    _unica_code = 'SVR1000'

    def __init__(self, msg):
        # fulfill _details
        self._details = self.unica_msg.format(msg)


class MissingMandatoryParameterException(ServiceDirectoryException):
    _unica_code = 'SVC1000'

    def __init__(self, parameter):
        # fulfill _details
        self._details = self.unica_msg.format(parameter)


class BadParameterException(ServiceDirectoryException):
    _unica_code = 'SVC1001'

    def __init__(self, parameter):
        # fulfill _details
        super(BadParameterException, self).__init__(self.unica_msg.format(parameter))


class DuplicatedParameterException(ServiceDirectoryException):
    _unica_code = 'SVC1024'

    def __init__(self, parameter):
        # fulfill _details
        super(DuplicatedParameterException, self).__init__(self.unica_msg.format(parameter))


class BadParameterValueException(ServiceDirectoryException):
    _unica_code = 'SVC0002'

    def __init__(self, parameter_value, details=None):
        if not details:
            if parameter_value == '':
                parameter_value = 'empty-string'
            details = self.unica_msg.format(parameter_value)
        super(BadParameterValueException, self).__init__(details)

    @staticmethod
    def get_regex_unica_code():
        """
        Helper method to return a regex representation of the intenal unica message
        for this exception class
        """
        unica_msg = ERRORS[BadParameterValueException._unica_code]['details']
        return '^{0}'.format(unica_msg.format(''))


class NotAllowedParameterValueException(ServiceDirectoryException):
    _unica_code = 'SVC0003'

    def __init__(self, parameter_value, allowed, details=None):
        # fulfill _details
        if not details:
            details = self.unica_msg.format(parameter_value, allowed)
        super(NotAllowedParameterValueException, self).__init__(details)

    @staticmethod
    def get_regex_unica_code():
        """
        Helper method to return a regex representation of the intenal unica message
        for this exception class
        """
        unica_msg = ERRORS[NotAllowedParameterValueException._unica_code]['details']
        return '^{0}'.format(unica_msg.format('(.*)', '(.*)'))


class UnsupportedParameterValueException(ServiceDirectoryException):
    _unica_code = 'SVC1021'

    def __init__(self, parameter_value, supported):
        # fulfill _details
        super(UnsupportedParameterValueException, self).__init__(self.unica_msg.format(parameter_value, supported))


class BadRequestException(ServiceDirectoryException):
    _unica_code = 'SVC0001'

    def __init__(self, parameter_value):
        # fulfill _details
        super(BadRequestException, self).__init__(self.unica_msg.format(parameter_value))


class NotFoundException(ServiceDirectoryException):
    _unica_code = 'SVC1006'

    def __init__(self, resource_name):
        # fulfill _details
        super(NotFoundException, self).__init__(self.unica_msg.format(resource_name))
