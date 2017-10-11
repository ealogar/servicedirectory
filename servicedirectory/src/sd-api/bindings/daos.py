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
from pymongo import ASCENDING

logger = logging.getLogger(__name__)


class BindingDao(BaseDao):
    """
    Dao to handle 'Bindings' collection documents
    """
    coll = "bindings"

    def __init__(self, *args, **kwargs):
        super(BindingDao, self).__init__(*args, **kwargs)
        # Ensure unique index in bindings collection is created
        self.dbcoll.ensure_index([("class_name", ASCENDING), ("origin", ASCENDING)],
                                 unique=True, name='class_name_origin')

    def find(self, binding_id):
        try:
            instance_id = ObjectId(binding_id)
            return super(BindingDao, self).find(instance_id)
        except (InvalidId, TypeError):
            return None

    def find_bindings(self, query_obj):
        return list(self.dbcoll.find(query_obj))

    def find_by_class_and_origin(self, class_name, origin):
        return self.dbcoll.find_one({'class_name': class_name, 'origin': origin})

    def update_binding(self, binding):
        """
        Update the given binding by _id and return True if document updated
            _Write Concern Not Supported. Default w=1. We use the following params:
                upsert=False Do not create the object if document does not exists.
                new=True Return the updated object and not the original
        :param binding The instance document to be modified
        :return True if object updated of false if not
        """
        binding_2_update = binding.copy()
        try:
            binding_id = ObjectId(binding_2_update.pop('_id'))
        except InvalidId:
            return False
        # update will launch DuplicateKeyError
        update_ret = self.dbcoll.update({'_id': binding_id},
                                        binding_2_update, upsert=False)
        return update_ret.get('ok') and update_ret.get('updatedExisting')

    def delete(self, binding_id):
        try:
            return super(BindingDao, self).delete(ObjectId(binding_id))
        except InvalidId:
            return False
