
from unittest import TestCase
from commons.utils import convert_str_to_type, pretty_type


class Test(TestCase):

    def test_conver_string_to_boolean_should_work(self):
        self.assertEquals(True, convert_str_to_type('true', bool), 'true can not be converted to boolean')
        self.assertEquals(False, convert_str_to_type('false', bool), 'false can not be converted to boolean')
        self.assertEquals(None, convert_str_to_type('t', bool), 't can be converted to boolean')

    def test_conver_string_to_float_should_work(self):
        self.assertEquals(1.0, convert_str_to_type('1.0', float), '1,0 can not be converted to float')
        self.assertEquals(None, convert_str_to_type('1', bool), '1 can be converted to float')
        self.assertEquals(None, convert_str_to_type('1.a', bool), '1.a can be converted to float')

    def test_conver_string_to_basestrings_should_work(self):
        self.assertEquals('test', convert_str_to_type('test', str), 'test can not be converted to str')
        self.assertEquals(u'test', convert_str_to_type('test', unicode), 'test can not be converted to unicode')

    def test_conver_string_to_long_should_return_none(self):
        self.assertEquals(None, convert_str_to_type('1', long), '1 can be converted to long')

    def test_pretty_type_should_work(self):
        self.assertEquals('boolean', pretty_type(True), 'pretty_type failed')
        self.assertEquals('integer', pretty_type(1), 'pretty_type failed')
        self.assertEquals('number', pretty_type(1.2), 'pretty_type failed')
        self.assertEquals('string', pretty_type('Hi there'), 'pretty_type failed')
        self.assertEquals('string', pretty_type(u'Hi there'), 'pretty_type failed')
        self.assertEquals('long', pretty_type(23L), 'pretty_type failed')
