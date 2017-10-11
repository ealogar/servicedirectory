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
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from commons.exception_mapper.exception_mapper import ExceptionMapper
import logging
from functools import wraps
from commons.exceptions import NotFoundException, DuplicatedParameterException,\
    GenericServiceError, BadParameterValueException, BadParameterException
from django.http.response import HttpResponse
from json import dumps
from itertools import imap
from re import match
from commons import local_context

logger = logging.getLogger(__name__)


def check_duplicated_query_params(f):
    """
    Utility decorator to check request query parameters in get
    does not have multiple values.
    If multiple values found, a bad request is raised
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        request = args[1]
        lowercase_keys = []
        for key in request.QUERY_PARAMS:
            if key.lower() in lowercase_keys or len(request.QUERY_PARAMS.getlist(key)) > 1:
                raise DuplicatedParameterException(key)
            lowercase_keys.append(key.lower())
        return f(*args, **kwargs)
    return wrapper


def check_empty_query_params(f):
    """
    Utility decorator to check request query parameters in get
    does not have empty value.
    If empty value is found, a bad request is raised
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        request = args[1]
        if any(imap(lambda x: x == '', request.QUERY_PARAMS.values())):
            raise BadParameterValueException('empty-query-parameter')
        return f(*args, **kwargs)
    return wrapper


def check_regex_query_params(regex):
    """
    Utility decorator to check request query parameters in get
    match the regex given.
    If some query parameter does not match, a bad request is raised
    """
    def applyDecorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            request = args[1]
            for key in request.QUERY_PARAMS.keys():  # not transform query params here for response msg
                if not match(regex, key.lower()):  # we allow uppercase query_params
                    raise BadParameterException(key)
            return f(*args, **kwargs)
        return wrapper
    return applyDecorator


class CustomGenericAPIView(GenericAPIView):
    """
    Overrides GenericAPIView to avoid handle exceptions. This will be
    done in another separate layer
    """

    def get_service(self):
        """
        Returns a new instance of the service_class defined in the view.
        When no service_class attribute is defined a GenericServiceError is raised.
        """
        if not hasattr(self, 'service_class'):
            logger.critical('%s must define a service_class attribute', self.__class__.__name__)
            raise GenericServiceError('Internal server error. Try again later')

        return self.service_class()

    # make get_service method available as a property in views
    service = property(get_service)

    def handle_exception(self, exc):
        # Call super method to handle_exception

        try:
            resp = super(CustomGenericAPIView, self).handle_exception(exc)
        except Exception as e:
            logger.warn(str(e))
            resp = Response()

        # Exception Mapper.
        # Provide kw args needed for formatting
        op_type = getattr(local_context, 'op_type', '')
        media_type = self.request.META.get('CONTENT_TYPE', '')
        exc_info = ExceptionMapper().get_exception_info(exc, op_type=op_type, media_type=media_type)
        if exc_info['details']:
            custom_data = {'exceptionId': exc_info['code'], 'exceptionText': exc_info['details']}
        else:
            # empty body
            custom_data = None

        resp.status_code = exc_info['status_code']
        # Update Error response with custom and localized data
        resp.data = custom_data
        return resp

    def get_serializer_context(self):
        """
        We provide kwargs of view as arguments in serializer context
        for a later easy access
        """
        context = super(CustomGenericAPIView, self).get_serializer_context()
        # get kwargs of View and include them in context
        if hasattr(self, 'kwargs'):
            context.update(getattr(self, 'kwargs', {}))
        return context

    def get_serializer_class(self):
        """
        Override default to allow serializer class per method.
        For example, to use a different serializer in post you should define:
               serializer_class_post = MyPostSerializer
        """
        serializer_class = getattr(self, 'serializer_class_%s' % self.request.method.lower(), None)
        if serializer_class is None:
            serializer_class = GenericAPIView.get_serializer_class(self)
        return serializer_class

    def lower_query_params(self, request, exclude=None):
        """
        Transform the request query_params given to lowercase excluding those keys
        presented in exclude and returns a dictionary
        """
        if exclude is None:
            exclude = ()
        request_params = dict(((key.lower(), value) for key, value in request.QUERY_PARAMS.items()
                                                        if key not in (exclude,)))
        return request_params


def handle_default_404(request):
    """
    Generic function basede view for deal with default 404 error
    launched by django (mainly url path not found)
    """

    # Exception Mapper.
    exc_info = ExceptionMapper().get_exception_info(NotFoundException(request.path))
    exc_data = {'exceptionId': exc_info['code'], 'exceptionText': exc_info['details']}
    return HttpResponse(content=dumps(exc_data), mimetype='application/json', status=exc_info['status_code'])


def handle_default_500(request):
    """
    Generic function based view for deal with default 500 error
    launched by django
    """

    exc_info = ExceptionMapper().get_exception_info(GenericServiceError('Internal error'))
    exc_data = {'exceptionId': exc_info['code'], 'exceptionText': exc_info['details']}
    return HttpResponse(content=dumps(exc_data), mimetype='application/json', status=exc_info['status_code'])
