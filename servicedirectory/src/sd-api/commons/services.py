'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
from commons.singleton import Singleton
from commons.exceptions import NotFoundException
import logging
import functools
from django.conf import settings
from commons.metaclasses import decorate_methods
from re import search
from commons.decorators import log_function_decorator

logger = logging.getLogger(__name__)


def return_obj_or_raise_not_found(f):
    """
    Utility method for handling None responses in service:
        When obj is None, a default NotFoundException is generated and raised
        The first input parameter value to the function is used to generate message
        Otherwise, the obj is returned
    """
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        obj = f(*args, **kwargs)
        if not obj:
            resource = ''
            if len(args) > 1:
                resource = args[1]
            raise NotFoundException(resource)
        return obj

    return wrapper


def apply_log_services_decorator(name, function):
    """
    We apply log decorator depending on settings
    """
    log_method = settings.DEFAULT_LOG_METHOD
    if hasattr(settings, 'LOG_METHOD_SERVICES'):
        log_method = settings.LOG_METHOD_SERVICES

    # We apply decorator if services is defined to be decorated and exclude
    # methods starting with __ (__init__, __new__)
    if 'services' in settings.LOG_LAYERS and not search(r'^__*', name):
        # we use the logger defined in this module
        return log_function_decorator(log_method, __name__)(function)
    return function


class SDServicesMetaclass(decorate_methods(apply_log_services_decorator), Singleton):
    """
    Metaclass for Services whic combine the decorateMethods metaclass and Singleton metaclass.
    It used the __new__ method of decorateMethods and the __call__ method of Singleton.
    """


class BaseService(object):
    __metaclass__ = SDServicesMetaclass
