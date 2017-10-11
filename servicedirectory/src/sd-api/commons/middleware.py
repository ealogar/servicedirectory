'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
import uuid
from django.conf import settings
import logging
from commons import local_context
from django.http.response import HttpResponsePermanentRedirect
from commons.exceptions import GenericServiceError

logger = logging.getLogger(__name__)


class UnicaCorrelatorMiddleware(object):
    """
    Middleware class to add to local thread a unique correlator id to be used
    in logging.
    It also includes the correlator_id in response headers.
    When the UNICA_CORRELATOR_HEADER is provided in request, that value is used, otherwise a unique
    identifier is generated.
    """

    def __init__(self):
        try:
            self.corr_req_header = settings.UNICA_CORRELATOR_REQUEST_HEADER
            self.corr_resp_header = settings.UNICA_CORRELATOR_RESPONSE_HEADER
            logger.info("Unica correlator headers readed")
        except AttributeError:
            logger.error("Unica Correlator headers not defined in settings")
            self.corr_req_header = self.corr_resp_header = None

    def process_request(self, request):
        if self.corr_req_header:
            request_correlator_id = self._get_request_correlator_id(request)
            local_context.correlator_id = request_correlator_id
        return None

    def _get_request_correlator_id(self, request):
        meta = request.META
        return meta.get(self.corr_req_header, self._generate_id())

    def _generate_id(self):
        return uuid.uuid4().hex

    def process_response(self, request, response):
        if self.corr_resp_header:
            # add new header to response with correlator_id
            response[self.corr_resp_header] = local_context.correlator_id
        return response


class TransactionIdMiddleware(object):
    """
    Middleware class to add to local thread a unique transaction id to be used
    in logging.
    A new transaction id is generated with every new request.
    """

    def process_request(self, request):
        local_context.transaction_id = uuid.uuid4().hex
        return None


class OperationTypeMiddleware(object):
    """
    Middleware class to add to local thread the operation type of the request
    based on the request method and the view name.
    """
    OP = {
        'GET-ServiceClassCollectionView': 'ListClasses',
        'POST-ServiceClassCollectionView': 'CreateClass',
        'GET-ServiceClassItemView': 'ListClass',
        'POST-ServiceClassItemView': 'UpdateClass',
        'DELETE-ServiceClassItemView': 'RemoveClass',
        'GET-ServiceInstanceView': 'SearchInstances',
        'POST-ServiceInstanceView': 'CreateInstance',
        'GET-ServiceInstanceItemView': 'ListInstance',
        'PUT-ServiceInstanceItemView': 'UpdateInstance',
        'DELETE-ServiceInstanceItemView': 'RemoveInstance',
        'GET-InfoView': 'Info',
        'GET-BindingsCollectionView': 'GetClassRules',
        'POST-BindingsCollectionView': 'CreateClassRules',
        'GET-BindingsItemView': 'ListClientRules',
        'PUT-BindingsItemView': 'UpdateClientRules',
        'DELETE-BindingsItemView': 'RemoveClientRules',
        'GET-UsersCollectionView': 'ListUsers',
        'POST-UsersCollectionView': 'CreateUser',
        'GET-UsersItemView': 'ListUser',
        'POST-UsersItemView': 'UpdateUser',
        'DELETE-UsersItemView': 'RemoveUser',
        'GET-BindingInstanceView': 'BindServiceInstance'
    }

    def process_view(self, request, view_func, view_args, view_kwargs):
        op_key = '{0}-{1}'.format(request.REQUEST.get('_method', request.method), view_func.func_name)
        local_context.op_type = self.OP.get(op_key, op_key)
        return None


class SSLRedirectMiddleware(object):
    """
    Middleware class to redirect incoming request to the correct protocol (from http to https)
    based on SSL keyword of view.
    """

    def process_view(self, request, view_func, view_args, view_kwargs):
        secure = False
        if 'SSL' in view_kwargs:
            secure = view_kwargs['SSL']

        # When access to secured view is not with secure protocol, redirect if possible
        if not self._is_secure(request) and secure is True:
            return self._redirect2_https(request, secure)

    def _is_secure(self, request):
        if request.is_secure():
            return True

        # Handle redirect from http to https ...
        if 'HTTP_X_FORWARDED_SSL' in request.META:
            return request.META['HTTP_X_FORWARDED_SSL'] == 'on'

        return False

    def _redirect2_https(self, request, secure):
        newurl = "https://{}{}".format(request.get_host(), request.get_full_path())
        if request.method == 'POST':
            raise GenericServiceError(u"Can not redirect to https in POST method. Make call with https")

        logger.debug("redirecting request to %s", newurl)
        return HttpResponsePermanentRedirect(newurl)


class MultipleProxyMiddleware(object):
    """
    Middleware to handle request.get_host when django is behind several proxies.
    Useful when dealing with redirects.
    """
    FORWARDED_FOR_FIELDS = [
        'HTTP_X_FORWARDED_FOR',
        'HTTP_X_FORWARDED_HOST',
        'HTTP_X_FORWARDED_SERVER',
    ]

    def process_request(self, request):
        """
        Rewrites the proxy headers so that only the most
        recent proxy is used.
        """
        for field in self.FORWARDED_FOR_FIELDS:
            if field in request.META:
                if ',' in request.META[field]:
                    parts = request.META[field].split(',')
                    request.META[field] = parts[-1].strip()
