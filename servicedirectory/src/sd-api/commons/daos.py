'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''

# Django imports
from django.conf import settings
# PyMongo imports
from pymongo import ReadPreference
from pymongo.errors import AutoReconnect, ConnectionFailure
from pymongo.mongo_client import MongoClient
import logging
from commons.singleton import Singleton
from re import search
from commons.decorators import log_function_decorator, retry
from commons.metaclasses import decorate_methods
from commons.exceptions import GenericServiceError

logger = logging.getLogger(__name__)


class MongoConnection(object):
    """
    Class to get a connection to the Mongo SGDB
    """
    __metaclass__ = Singleton

    _db_connection = None

    def __init__(self, **dbconfig):
        self.dbconfig = dbconfig or settings.MONGODB
        try:
            if self.dbconfig["slave_ok"]:
                read_preference = ReadPreference.NEAREST
            else:
                read_preference = ReadPreference.PRIMARY

            # Initialize MongoClient connection
            self._db_connection = MongoClient(self.dbconfig["hosts"],
                                        w=self.dbconfig["replicaset_number"],
                                        replicaset=self.dbconfig["replicaset"],
                                        read_preference=read_preference,
                                        auto_start_request=self.dbconfig["autostart"])
            logger.info("Connection to the mongodb started")
        except AutoReconnect as e:
            logger.warning("It has not been possible to connect to all the hosts %s", str(e))
        except ConnectionFailure as es:
            logger.critical("It has not been possible to start the connection to the hosts %s", str(es))
            raise GenericServiceError("Internal error. Try again later")

    def get_db_connection(self, db_name=None):
        '''Retrieve a DB connection
        :param dbname: database name
        '''
        db_name = db_name or self.dbconfig["dbname"]
        return self._db_connection[db_name]


def apply_log_daos_decorator(name, function):
    """
    We apply log decorator depending on settings
    """
    log_method = settings.DEFAULT_LOG_METHOD
    if hasattr(settings, 'LOG_METHOD_DAOS'):
        log_method = settings.LOG_METHOD_DAOS

    # We apply decorator if daos is defined to be decorated and exclude
    # methods starting with __ (__init__, __new__)
    if 'daos' in settings.LOG_LAYERS and not search(r'^__*', name):
        # We use __name__ as logger name
        return log_function_decorator(log_method, __name__)(function)
    return function


def apply_retry_decorator(name, function):
    """
    We apply retry decorator depending on common settings.
    """
    functions_to_retry = settings.RETRY_FUNCTIONS_DAOS
    backoff_daos = settings.BACKOFF_OP_DAOS
    delay_daos = settings.DELAY_OP_DAOS
    max_retries = settings.MAX_RETRIES_DAOS

    for pattern in functions_to_retry:
        if search(pattern, name):
            return retry(backoff_daos, delay_daos, max_retries, (AutoReconnect,), __name__)(function)
    return function


class BaseDao(object):
    """
    DAO holding basic common DAO features.
    Subclasses must define a coll property.
    Every method beginning by get, find, update and delete
    will handle AutoReconnect to retry the operation ( see retry decorator)
    """
    __metaclass__ = decorate_methods(apply_log_daos_decorator, apply_retry_decorator)

    def __init__(self):
        if not hasattr(self, 'coll'):
            raise NotImplementedError("{0}.coll method must defined when overriding".format(self.__class__.__name__))
        self.dbconn = MongoConnection().get_db_connection()
        self.dbcoll = self.dbconn[self.coll]

    def find_all(self):
        '''
        Find all document in collection
        :returns cursor with retrieved documents (can be iterated)
        '''
        dbdoc = self.dbcoll.find()
        return list(dbdoc)

    def create(self, obj):
        """
        Creates a new object in mongo dabatase

        :param obj Object to be created in mongo with _id inside
        :return created object in mongo
        :raises DuplicateKeyException if object is already created
        """
        self.dbcoll.insert(obj)
        return obj

    def delete(self, obj_id):
        res = self.dbcoll.remove({'_id': obj_id})
        return (res.get('ok', False) and res.get('n', 0) == 1)

    def find(self, obj_id):
        return self.dbcoll.find_one({'_id': obj_id})
