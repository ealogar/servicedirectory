'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
from commons.daos import BaseDao
import logging

logger = logging.getLogger(__name__)


class UserAdminDao(BaseDao):
    """
    Dao to handle users credentials for sd rest class.
    In mongo we hold a document with attributes being the same
    as django.contrib.auth.models.User in order that rest_framework
    utilities for auth will continue to work.
    """

    coll = 'users'

    def find(self, username):
        """
        Check for User in database with _id=username and password = hashed(password)
        and returns a AttrDict of the document.
        AttrDict allows access of keys with dot notation and may be used inside django.
        """
        return self.dbcoll.find_one({'_id': username})

    def create(self, username, hashed_password, is_admin, classes, origins):
        # Store a custom dict with enconded password in database
        user = {'_id': username, 'password': hashed_password,
                'is_admin': is_admin, 'classes': classes, 'origins': origins}

        return super(UserAdminDao, self).create(user)

    def update(self, user):
        """
        Update a user in database and returns True.
        If any user is updated False is returned
        When a database operation happens, OperationFailure is raised by mongodb
        """
        user_2_update = user.copy()
        update_ret = self.dbcoll.update({'_id': user_2_update.pop('_id')},
                                   user_2_update,
                                      upsert=False)
        if update_ret.get('ok') and update_ret.get('updatedExisting'):
            return True
        else:
            return False
