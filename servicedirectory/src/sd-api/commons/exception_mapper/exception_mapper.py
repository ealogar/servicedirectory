'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
from commons.exception_mapper.errors.errors import ERRORS
from commons.exception_mapper.errors.exception_translator import EXCEPTIONS, DEFAULT_EXCEPTION
import logging
from commons.singleton import Singleton
from commons.exceptions import ServiceDirectoryException
import traceback
from django.conf import settings

logger = logging.getLogger(__name__)


class ExceptionMapper(object):

    __metaclass__ = Singleton

    def get_exception_info(self, exception, **kwargs):
        try:
            if settings.TRACE_EXCEPTIONS:
                logger.debug("Handling %s", traceback.format_exc())
        except AttributeError:
            pass  # We pass because is just a trace message
        exception_name = exception.__class__.__name__
        if not isinstance(exception, ServiceDirectoryException):
            exc_info = self.translate_exception(exception_name, str(exception), **kwargs)
        else:
            exc_info = {
                'exception_name': exception_name,
                'code': exception.code,
                'details': exception._details,
                'status_code': exception.status_code
            }

        # Log all exception before returning to client
        if exc_info['status_code'] == 500:  # log this as error (General Failure)
            log_method = logger.error
        else:
            log_method = logger.info
        log_method("Error in request with code %s: %s", exc_info['code'], exc_info['details'])
        return exc_info

    def translate_exception(self, exception_name, exception_text, op_type='', media_type=''):
        """
        Utility method to get all exception info needed to generate json response for
        third parties (rest_framework, django, etc.).
        """

        logger.debug('Searching exception information of %s', exception_name)

        if exception_name in EXCEPTIONS:
            exception = EXCEPTIONS[exception_name].copy()
        else:
            exception = EXCEPTIONS[DEFAULT_EXCEPTION].copy()

        error_info = ERRORS[exception['code']].copy()

        exc_info = {
            'exception_name': exception_name,
            'code': exception['code'],
            'details': error_info['details'],
            'status_code': int(error_info['status_code'])  # status_code must be integer
        }
        if exc_info['details']:
            # Include op_type in PermissionDenied and MethodNotAllowed exception
            if exc_info['exception_name'] in ('PermissionDenied', 'MethodNotAllowed'):
                exc_info['details'] = exc_info['details'].format(op_type)
            # Include media_type in UnsupportedMediaType exception
            if exc_info['exception_name'] == 'UnsupportedMediaType':
                exc_info['details'] = exc_info['details'].format(media_type)
            # Include message in genericError
            if exc_info['exception_name'] == 'GenericServiceError':
                exc_info['details'] = exc_info['details'].format(exception_text)
            if exc_info['exception_name'] not in EXCEPTIONS:
                exc_info['details'] = exc_info['details'].format('internal error')

        return exc_info
