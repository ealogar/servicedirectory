'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
import logging
from commons import local_context


class TransactionIDFilter(logging.Filter):

    def filter(self, record):
        record.transaction_id = getattr(local_context, 'transaction_id', 'NA')
        return True


class CorrelatorIDFilter(logging.Filter):

    def filter(self, record):
        record.correlator_id = getattr(local_context, 'correlator_id', 'NA')
        return True


class OpTypeFilter(logging.Filter):

    def filter(self, record):
        record.op_type = getattr(local_context, 'op_type', 'NA')
        return True


class LevelNameFilter(logging.Filter):
    TDAF_LEVELS = {
                  'WARNING': 'WARN',
                  'CRITICAL': 'FATAL'
    }

    def filter(self, record):
        record.tdaf_levelname = self.TDAF_LEVELS.get(record.levelname, record.levelname)
        return True
