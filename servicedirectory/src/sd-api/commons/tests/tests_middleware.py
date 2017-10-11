from unittest import TestCase
from commons.middleware import UnicaCorrelatorMiddleware, SSLRedirectMiddleware,\
    MultipleProxyMiddleware
from mock import patch, ANY, MagicMock
from django.http.response import HttpResponsePermanentRedirect


class Test(TestCase):

    def test_correlator_headers_not_in_settings_should_write_error(self):

        class SettingsMock(object):
            pass

        settings_mock = SettingsMock()
        with patch('commons.middleware.settings', new=settings_mock) as settings_mock,\
             patch('commons.middleware.logger') as logger_mock:
            unica_mid = UnicaCorrelatorMiddleware()
            logger_mock.error.assert_called_once_with(ANY)
            request = MagicMock(name='request_mock')
            del request.META  # provoke an attributeError if Meta is called...
            self.assertEquals(None, unica_mid.process_request(request))

            response = {'my_key': 'una'}
            self.assertEquals(response, unica_mid.process_response(request, response))

    def test_ssl_middleware_should_redirect_secured_view(self):

        ssl_mid = SSLRedirectMiddleware()
        request = MagicMock(name='request_mock')
        request.is_secure.return_value = False
        view_func = MagicMock(name='view_mock')
        resp = ssl_mid.process_view(request, view_func, (), {'SSL': True})

        self.assertTrue(isinstance(resp, HttpResponsePermanentRedirect))

    def test_ssl_middleware_should_handle_redirect2_secured(self):

        ssl_mid = SSLRedirectMiddleware()
        request = MagicMock(name='request_mock')
        request.is_secure.return_value = False
        request.META = {'HTTP_X_FORWARDED_SSL': 'on'}
        view_func = MagicMock(name='view_mock')
        resp = ssl_mid.process_view(request, view_func, (), {'SSL': True})

        self.assertTrue(resp is None)

    def test_ssl_middleware_should_not_redirect_unsecured_view(self):

        ssl_mid = SSLRedirectMiddleware()
        request = MagicMock(name='request_mock')
        request.is_secure.return_value = True
        view_func = MagicMock(name='view_mock')
        resp = ssl_mid.process_view(request, view_func, (), {'SSL': False})

        self.assertTrue(resp is None)

    def test_multiple_proxy_should_leave_only_first(self):

        multiple_mid = MultipleProxyMiddleware()
        request = MagicMock(name='request_mock')
        request.META = {'HTTP_X_FORWARDED_FOR': 'first_address,last_address'}
        multiple_mid.process_request(request)

        self.assertEquals('last_address', request.META['HTTP_X_FORWARDED_FOR'])
