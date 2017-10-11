'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
from django.test import TestCase as DjangoTestCase
from django.conf import settings
from django.test.utils import override_settings
from commons.daos import MongoConnection
from classes.services import ServiceInstanceService, ServiceClassService
from commons.singleton import Singleton
import base64

# Chage mongodb to settings for testing
_MONGODB = settings.MONGODB
_MONGODB['dbname'] = ''.join([_MONGODB['dbname'], '_testing'])


@override_settings(MONGODB=_MONGODB)
class TestCase(DjangoTestCase):

    ADMIN_AUTH = 'Basic ' + base64.b64encode('%s:%s' % ('admin', 'admin'))

    @classmethod
    def setUpClass(cls):
        # Remove singleton to start again connection against database of tests
        Singleton._instances = {}
        # call init of services (not being called in views again)
        ServiceInstanceService()
        ServiceClassService()

    @classmethod
    def tearDownClass(cls):
        # Remove all collections in database tests
        conn = MongoConnection()
        db = conn._db_connection
        db.drop_database(conn.get_db_connection())

    def get(self, *args, **kwargs):
        return self.client.get(*args, content_type='application/json',
                               HTTP_USER_AGENT='Test-Agent', **kwargs)

    def put(self, *args, **kwargs):
        if 'HTTP_AUTHORIZATION' not in kwargs:
            kwargs['HTTP_AUTHORIZATION'] = self.ADMIN_AUTH
        elif kwargs['HTTP_AUTHORIZATION'] == None:
            kwargs.pop('HTTP_AUTHORIZATION')
        return self.client.put(*args, content_type='application/json',
                               HTTP_USER_AGENT='Test-Agent', **kwargs)

    def post(self, *args, **kwargs):
        if 'HTTP_AUTHORIZATION' not in kwargs:
            kwargs['HTTP_AUTHORIZATION'] = self.ADMIN_AUTH
        elif kwargs['HTTP_AUTHORIZATION'] == None:
            kwargs.pop('HTTP_AUTHORIZATION')
        return self.client.post(*args, content_type='application/json',
                               HTTP_USER_AGENT='Test-Agent', **kwargs)

    def delete(self, *args, **kwargs):
        if 'HTTP_AUTHORIZATION' not in kwargs:
            kwargs['HTTP_AUTHORIZATION'] = self.ADMIN_AUTH
        elif kwargs['HTTP_AUTHORIZATION'] == None:
            kwargs.pop('HTTP_AUTHORIZATION')
        return self.client.delete(*args, content_type='application/json',
                               HTTP_USER_AGENT='Test-Agent', **kwargs)


class DictMatcher:

    def __init__(self, expected, unexpected_keys=[]):
        self.expected = expected
        self.unexpected_keys = unexpected_keys
        self.key_error = None
        self.value_error = None

    def compare_list(self, expected, other):
        for e in expected:
            if e not in other:
                return False
        return True

    def compare_dicts(self, expected, other):
        for key, value in expected.items():
            if key not in other:
                return False
            else:
                if isinstance(value, list):
                    if self.compare_list(value, other[key]) is False:
                        return False
                else:
                    if other[key] != value:
                        return False
        return True

    def __eq__(self, other):
        for key, value in self.expected.items():
            if key not in other:
                self._error = 'expected key {0} not found'.format(key)
                return False
            else:
                if isinstance(value, dict):
                    if self.compare_dicts(value, other[key]) is False:
                        self._error = 'the dict key {0} should have {1} value'.format(key, str(value))
                        return False
                else:
                    if other[key] != value:
                        self._error = 'the key {0} should have {1} value'.format(key, str(value))
                        return False
        for key in self.unexpected_keys:
            if key in other:
                self._error = 'unexpected key {0}'.format(key)
                return False

        return True

    def __unicode__(self):
        return getattr(self, '_error', 'error')

    def __str__(self):
        return unicode(self).encode('utf-8')
    __repr__ = __unicode__
