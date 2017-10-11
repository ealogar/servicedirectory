'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
from commons.exceptions import GenericServiceError, UnsupportedParameterValueException
from commons.services import BaseService, return_obj_or_raise_not_found
from users.daos import UserAdminDao
from pymongo.errors import DuplicateKeyError
import logging
from django.conf import settings
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import PermissionDenied
from classes.daos import ServiceClassDao


logger = logging.getLogger(__name__)


class UserAdminService(BaseService):

    def __init__(self):
        self.dao = UserAdminDao()
        self.classes_dao = ServiceClassDao()

    def get_all_users(self):
        return self.dao.find_all()

    @return_obj_or_raise_not_found
    def get_user(self, username):
        return self.dao.find(username)

    def validate_classes(self, classes):
        """
        Check that the given classes exist in SD
        """
        for class_ in classes:
            if self.classes_dao.find(class_) is None:
                raise UnsupportedParameterValueException(class_, 'existing-class')

    def create(self, user):
        self.validate_classes(user.get('classes', ()))
        try:
            return self.dao.create(user['_id'], make_password(user['password']),
                                   user.get('is_admin', False), user.get('classes', ()),
                                   user.get('origins', ()))
        except DuplicateKeyError:
            raise UnsupportedParameterValueException(user['_id'], 'non-existing-user')

    def update(self, user, auth_username):
        # user exist validation in serializer
        # Can not update himself
        if user['_id'] == auth_username:
            raise PermissionDenied('Admin user can not update himself.')

        self.validate_classes(user.get('classes', ()))
        if self.dao.update(user):  # if OperationFailure is raised, the exception mapper will translate
            return user
        else:
            raise GenericServiceError('User update failed')

    def delete(self, username, auth_username):
        # Ensure user exists
        self.get_user(username)
        if username == settings.SD_USERNAME:
            raise PermissionDenied('default user can not be deleted.')
        elif username == auth_username:
            raise PermissionDenied('Admin user can not delete himself.')

        if self.dao.delete(username) is False:
            raise GenericServiceError('User update failed')
