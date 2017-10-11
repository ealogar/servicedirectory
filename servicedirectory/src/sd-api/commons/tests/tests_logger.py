
from unittest import TestCase
import commons.logger
from commons.decorators import log_function_decorator
reload(commons.logger)
from mock import MagicMock
from commons import local_context


class Test(TestCase):

    def test_transaction_id_filter(self):
        record_mock = MagicMock(name='log_mock')
        local_context.transaction_id = 'test_id'
        transacation_id_filter = commons.logger.TransactionIDFilter()
        res = transacation_id_filter.filter(record_mock)
        self.assertEquals(True, res, 'Transaction id filter not executed correctly')
        self.assertTrue(record_mock.transaction_id == 'test_id', "transaction_id was not added to log")

    def test_correlator_id_filter(self):
        record_mock = MagicMock(name='log_mock')
        local_context.correlator_id = 'test_id'
        corr_id_filter = commons.logger.CorrelatorIDFilter()
        res = corr_id_filter.filter(record_mock)
        self.assertEquals(True, res, 'Correlator id filter not executed correctly')
        self.assertTrue(record_mock.correlator_id == 'test_id', "correlator_id was not added to log")

    def test_op_type_filter(self):
        record_mock = MagicMock(name='log_mock')
        op_type_filter = commons.logger.OpTypeFilter()
        local_context.op_type = 'test-op'
        res = op_type_filter.filter(record_mock)
        self.assertEquals(True, res, 'op_type filter not executed correctly')
        self.assertTrue(record_mock.op_type == 'test-op', "op_type was not added to log")

    def test_tdaf_levelname_filter(self):
        record_mock = MagicMock(name='log_mock')
        record_mock.levelname = 'WARNING'
        tdaf_levelname_filter = commons.logger.LevelNameFilter()
        res = tdaf_levelname_filter.filter(record_mock)
        self.assertEquals(True, res, 'tdaf_levelname filter not executed correctly')
        self.assertTrue(record_mock.tdaf_levelname == 'WARN', "tdaf_levlname was not added to log")
        record_mock.levelname = 'CRITICAL'
        res = tdaf_levelname_filter.filter(record_mock)
        self.assertEquals(True, res, 'tdaf_levelname filter not executed correctly')
        self.assertTrue(record_mock.tdaf_levelname == 'FATAL', "tdaf_levlname was not added to log")
        record_mock.levelname = 'INFO'
        res = tdaf_levelname_filter.filter(record_mock)
        self.assertEquals(True, res, 'tdaf_levelname filter not executed correctly')
        self.assertTrue(record_mock.tdaf_levelname == 'INFO', "tdaf_levlname was not added to log")

    def test_log_funcion_decorator(self):
        class ServiceTest(object):

            @log_function_decorator()
            def method_with_just_kw_args(self, arg=23):
                pass

            @log_function_decorator()
            def method_with_args_and_kw(self, arg, arg2=90):
                pass

            @log_function_decorator()
            def method_with_just_args(self, arg):
                pass

            @log_function_decorator()
            def method_without_args(self):
                pass

        service_test = ServiceTest()
        service_test.method_with_args_and_kw(23, arg2=90)
        service_test.method_with_just_kw_args(arg=90)
        service_test.method_with_just_args(45)
        service_test.method_without_args()
