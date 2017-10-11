'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
from bson.objectid import ObjectId
from commons.daos import BaseDao
from bson.errors import InvalidId
import logging
from pymongo import DESCENDING, ASCENDING

logger = logging.getLogger(__name__)


class ServiceClassDao(BaseDao):
    """
    Dao to handle 'ServiceClasses' collection documents
    """
    coll = "serviceclasses"

    def __init__(self, *args, **kwargs):
        super(ServiceClassDao, self).__init__(*args, **kwargs)

    def update(self, obj):
        """
        Find a class document by class_name and update description and default version
        If the update is successful, True will be returned. If no update is performed,
        False is returned.
        When a database error happens, operationFailure is raised by pymongo driver
        :param class_name the name of the class to be find
        :param obj The partial class document to be modified
        :return the updated object or None if class_name does not exist
        """
        class_2_update = obj.copy()
        update_ret = self.dbcoll.update({'_id': class_2_update.pop('_id')},
                                          {'$set': class_2_update},
                                          upsert=False)
        return update_ret.get('ok') and update_ret.get('updatedExisting')


class ServiceInstanceDao(BaseDao):
    """
    Dao to handle the ServiceInstances for every ServiceClass
    """

    coll = "serviceinstances"

    def __init__(self, *args, **kwargs):
        super(ServiceInstanceDao, self).__init__(*args, **kwargs)
        # Ensure unique index in instances collection is created
        self.dbcoll.ensure_index([("class_name", ASCENDING), ("version", ASCENDING),
                                 ("uri", ASCENDING)], unique=True, name='class_name_uri_version')

    def find(self, obj_id):
        try:
            instance_id = ObjectId(obj_id)
            return super(ServiceInstanceDao, self).find(instance_id)
        except (InvalidId, TypeError):
            return None

    def find_by_class_name_and_id(self, class_name, obj_id):
        try:
            instance_id = ObjectId(obj_id)
            return self.dbcoll.find_one({'_id': instance_id, 'class_name': class_name})
        except (InvalidId, TypeError):
            return None

    def find_all(self, class_name):
        """
        Find all the instances under the Class "class_name"
        :param class_name name of the class to be used
        :return a list with the recovered instances
        """
        return list(self.dbcoll.find({'class_name': class_name}))

    def find_instances(self, query_obj):
        return list(self.dbcoll.find(query_obj).sort('version', DESCENDING))

    def update(self, obj):
        """
        Find a instance document by _id and update the object if found
            _Write Concern Not Supported. Default w=1. We use the following params:
                upsert=False Do not create the object if document does not exists.
                new=True Return the updated object and not the original
        :param obj The instance document to be modified
        :return True if the instance is updated, otherwise False
        """
        instance_2_update = obj.copy()
        try:
            instance_id = ObjectId(instance_2_update.pop('_id'))
        except InvalidId:
            return False
        # update will launch DuplicateKeyError
        update_ret = self.dbcoll.update({'_id': instance_id},
                                        instance_2_update, upsert=False)
        return update_ret.get('ok') and update_ret.get('updatedExisting')

    def delete(self, obj_id):
        try:
            return super(ServiceInstanceDao, self).delete(ObjectId(obj_id))
        except InvalidId:
            return False

    def delete_by_class_name(self, class_name):
        self.dbcoll.remove({'class_name': class_name})
