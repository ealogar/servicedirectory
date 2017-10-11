'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
import unittest
from mock import patch
from commons.exception_mapper.exception_mapper import ExceptionMapper
from commons.exceptions import ServiceDirectoryException


class UnknownException(Exception):

    def __init__(self, details):
        self._details = details

    def __str__(self):
        return repr(self._details)


class KnownException(ServiceDirectoryException):

    _unica_code = 'SVC0002'

    def __init__(self, param):
        self._details = self.unica_msg.format(param)


class NoSDException(Exception):

    def __init__(self, details):
        self._details = details


class ExceptionMapperTest(unittest.TestCase):

    ERRORS = {
        'SVC0001': {
            'details': 'My General Failure',
            'status_code': 500
        },
        'SVC0002': {
            'details': 'Resource {0} not found',
            'status_code': 404
        },
        'SVC0003': {
            'details': 'Some problem',
            'status_code': 400
        }
    }

    DEFAULT_EXCEPTION = 'GeneralException'

    EXCEPTIONS = {
        'GeneralException': {
            'code': 'SVC0001'
        },
        'NoSDException': {
            'code': 'SVC0003'
        }
    }

    exception_mapper = None

    def setUp(self):
        self.exception_mapper = ExceptionMapper()

    def test_exception_mapper_should_be_a_singleton(self):
        exc_mapper = ExceptionMapper()
        self.assertEquals(id(self.exception_mapper), id(exc_mapper))

    @patch('commons.exception_mapper.exception_mapper.ERRORS', ERRORS)
    @patch('commons.exception_mapper.exception_mapper.DEFAULT_EXCEPTION', DEFAULT_EXCEPTION)
    @patch('commons.exception_mapper.exception_mapper.EXCEPTIONS', EXCEPTIONS)
    def test_get_exception_info_unknown_exception_should_return_default_exception(self):
        exc_info = self.exception_mapper.get_exception_info(UnknownException('MyMsg'))
        self.assertEquals(500, exc_info['status_code'])
        self.assertEquals('SVC0001', exc_info['code'])
        self.assertEquals('UnknownException', exc_info['exception_name'])
        self.assertEquals('My General Failure', exc_info['details'])

    @patch('commons.exceptions.ERRORS', ERRORS)
    @patch('commons.exception_mapper.exception_mapper.ERRORS', ERRORS)
    @patch('commons.exception_mapper.exception_mapper.DEFAULT_EXCEPTION', DEFAULT_EXCEPTION)
    @patch('commons.exception_mapper.exception_mapper.EXCEPTIONS', EXCEPTIONS)
    def test_get_exception_info_known_exception_should_return_exception_code_unica(self):
        exc_info = self.exception_mapper.get_exception_info(KnownException('MyMsg'))
        self.assertEquals(404, exc_info['status_code'])
        self.assertEquals('SVC0002', exc_info['code'])
        self.assertEquals('KnownException', exc_info['exception_name'])
        self.assertEquals('Resource MyMsg not found', exc_info['details'])

    @patch('commons.exception_mapper.exception_mapper.ERRORS', ERRORS)
    @patch('commons.exception_mapper.exception_mapper.DEFAULT_EXCEPTION', DEFAULT_EXCEPTION)
    @patch('commons.exception_mapper.exception_mapper.EXCEPTIONS', EXCEPTIONS)
    def test_get_exception_info_exception_third_party_should_return_mapped_exception(self):
        exc_info = self.exception_mapper.get_exception_info(NoSDException('MyMsg'))
        self.assertEquals(400, exc_info['status_code'])
        self.assertEquals('SVC0003', exc_info['code'])
        self.assertEquals('NoSDException', exc_info['exception_name'])
        self.assertEquals('Some problem', exc_info['details'])
