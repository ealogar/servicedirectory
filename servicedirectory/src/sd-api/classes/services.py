'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
from __future__ import unicode_literals
import logging

from pymongo.errors import DuplicateKeyError, OperationFailure

from commons.exceptions import GenericServiceError, NotFoundException, \
    UnsupportedParameterValueException, BadParameterException
from commons.services import BaseService, return_obj_or_raise_not_found
from classes.daos import ServiceClassDao, ServiceInstanceDao
from bindings.daos import BindingDao

logger = logging.getLogger(__name__)


class ServiceClassService(BaseService):
    """
    Service to handle ServiceClass objects with mongodb and provide
    all business logic needed to views layer
    """

    def __init__(self):
        self.class_dao = ServiceClassDao()
        self.instance_dao = ServiceInstanceDao()

    def get_all_service_classes(self):
        return list(self.class_dao.find_all())

    def create(self, obj):
        try:
            return self.class_dao.create(obj)
        except DuplicateKeyError:
            raise UnsupportedParameterValueException(obj['_id'], 'non-existing-class')

    @return_obj_or_raise_not_found
    def get(self, class_name):
        return self.class_dao.find(class_name)

    def update(self, obj):
        # raise not found if not existing class

        if self.class_dao.update(obj):  # When OperationFailure, Exception mapper will translate
            return obj
        else:
            raise GenericServiceError('Class update failed')

    def delete(self, class_name):
        class_obj = self.class_dao.find(class_name)
        if class_obj:
            try:
                self.instance_dao.delete_by_class_name(class_name)
            except OperationFailure:
                raise GenericServiceError('The class delete process failed.')
            if self.class_dao.delete(class_name):
                return
            else:
                raise GenericServiceError('The class delete process failed.')

        raise NotFoundException(class_name)


class ServiceInstanceService(BaseService):
    """
    Service to handle ServiceInstance objects with mongodb and provide
    all business logic needed to views layer
    """

    def __init__(self):
        self.instance_dao = ServiceInstanceDao()
        self.class_dao = ServiceClassDao()
        self.binding_dao = BindingDao()

    def create(self, obj):
        if not self.class_dao.find(obj['class_name']):
            raise NotFoundException(obj['class_name'])
        try:
            return self.instance_dao.create(obj)
        except DuplicateKeyError:
            raise UnsupportedParameterValueException('{0}-{1}-{2}'.format(obj['class_name'],
                                                    obj['uri'], obj['version']), 'non-duplicated-instance')

    def get_service_instance(self, class_name, instance_id):
        class_obj = self.class_dao.find(class_name)
        if class_obj:
            instance = self.instance_dao.find(instance_id)
            if instance:
                if instance['class_name'] == class_name:
                    return instance
                else:
                    raise UnsupportedParameterValueException('{0}-{1}'.format(class_name, instance_id),
                                                     'instances-of-class')
            else:
                raise NotFoundException(instance_id)
        else:
            raise NotFoundException(class_name)

    def update(self, obj):
        # if not instance is found, not found would be raised in serializers
        try:
            if self.instance_dao.update(obj):
                return obj
            else:
                raise GenericServiceError('The instance update process failed.')
        except DuplicateKeyError:
            raise UnsupportedParameterValueException('{0}-{1}-{2}'.format(obj['class_name'], obj['uri'],
                                                    obj['version']), 'non-duplicated-instance')

    def delete(self, class_name, instance_id):
        class_obj = self.class_dao.find(class_name)
        if class_obj:
            instance = self.instance_dao.find(instance_id)
            if instance:
                if instance['class_name'] == class_name:
                    if self.instance_dao.delete(instance_id):
                        return
                    else:
                        raise GenericServiceError('The instance delete process failed.')
                else:
                    raise UnsupportedParameterValueException('{0}-{1}'.format(class_name, instance_id),
                                                             'instances-of-class')
            else:
                raise NotFoundException(instance_id)
        raise NotFoundException(class_name)

    def discover_service_instances(self, class_name, params):
        if 'class_name' in params:
            raise BadParameterException('class_name')
        class_obj = self.class_dao.find(class_name)
        if not class_obj:
            raise NotFoundException(class_name)
        params['class_name'] = class_name
        return self.instance_dao.find_instances(params)
