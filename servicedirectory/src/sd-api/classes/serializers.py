'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
from __future__ import unicode_literals  # Make all strings in file converted to unicode
import logging
from re import match

from django.conf import settings
from rest_framework.serializers import Serializer
from django.core.exceptions import ValidationError

import commons.serializers
from classes.services import ServiceInstanceService, ServiceClassService
from commons.exceptions import NotFoundException, \
    BadParameterValueException,\
    GenericServiceError
from commons.fields import CharRestrictField, error_messages, ObjectIdField, RegexRestricField
from commons.serializers import SchemaSerializer


logger = logging.getLogger(__name__)


class ServiceClassCollectionSerializer(SchemaSerializer):
    """
    Serializer class for serviceclass collection
    """
    class_name = RegexRestricField('^{0}$'.format(settings.CLASS_NAME_REGEX), min_length=1, max_length=512,
                                      source='_id', required=True)

    class Meta:
        schema = 'ClassModel'
        view_item_name = 'class_detail'
        # _id instead of 'class_name' because the source of class_name is _id
        url_fields = ('_id',)
        # _id field of schema will be mapped in class_name
        exclude = ('_id',)


class ServiceClassItemSerializer(ServiceClassCollectionSerializer):

    class_name = CharRestrictField(source='_id', read_only=True)  # read_onlye, validation not needed here

    def restore_object(self, attrs, instance=None):
        # Recover existing service class, notFound may be launched
        instance = ServiceClassService().get(self.context['class_name'])
        return super(ServiceClassItemSerializer, self).restore_object(attrs, instance=instance)


class AttributesSerializer(Serializer):
    """
    Serializer that allow dynamic char fields.
    """
    default_error_messages = error_messages

    def __init__(self, allowed_size=(0, 128), allowed_key_length=(1, 512), allowed_value_length=(1, 512), **kwargs):
        self.min_size = allowed_size[0]
        self.max_size = allowed_size[1]
        self.min_key_length = allowed_key_length[0]
        self.max_key_length = allowed_key_length[1]
        self.min_value_length = allowed_value_length[0]
        self.max_value_length = allowed_value_length[1]
        super(AttributesSerializer, self).__init__(**kwargs)

    def create_dynamic_fields(self, obj):
        if not getattr(self, '_errors', None):
            self._errors = {}
        field_mapping = {
            str: CharRestrictField,  # Only string is allowed as dynamic fields
            unicode: CharRestrictField
        }
        if not isinstance(obj, dict):
            bad_param = BadParameterValueException(obj)
            raise ValidationError(bad_param.details)
        # Min_size and max_size validations
        if len(obj) < self.min_size or len(obj) > self.max_size:
            bad_param = BadParameterValueException(obj)
            raise ValidationError(bad_param.details)

        for (key, value) in obj.items():
            # Key length validations (value is done as field...)
            if len(key) < self.min_key_length or len(key) > self.max_key_length:
                bad_param = BadParameterValueException(key)
                raise ValidationError(bad_param.details)

            if key not in self.fields:
                try:
                    if not match('^{0}$'.format(settings.ATTTRIBUTES_KEYS_REGEX), key):
                        bad_param = BadParameterValueException(key)
                        raise ValidationError(bad_param.details)
                    else:
                        field = field_mapping[type(value)](min_length=self.min_value_length,
                                                           max_length=self.max_value_length)
                        field.initialize(parent=self, field_name=key)
                        self.fields[key] = field
                except KeyError:
                    bad_param = BadParameterValueException(value)
                    raise ValidationError(bad_param.details)
            else:
                # fields already defined -> doesn't need to be created
                continue

    def restore_fields(self, data, files):
        """
        Override default to add fields to serializer dynamically
        """
        self.create_dynamic_fields(data)
        return super(AttributesSerializer, self).restore_fields(data, files)

    def to_native(self, obj):
        """
        Override to_native:
          add fields to serializer dynamically
          exclude fields with null value
          not all elements in serialization are provided
        """
        try:
            self.create_dynamic_fields(obj)
        except ValidationError:
            raise GenericServiceError('Attributes of class invalid')
        ret = self._dict_class()
        ret.fields = {}

        for field_name, field in self.fields.items():
            field.initialize(parent=self, field_name=field_name)
            key = self.get_field_key(field_name)
            if key not in obj:  # TODO when obj does not have optional key don't fill
                continue
            value = field.field_to_native(obj, field_name)
            ret[key] = value
            ret.fields[key] = field
        return ret


class ServiceInstanceSerializer(commons.serializers.ExcludeFieldMixing, commons.serializers.SchemaSerializer):
    """
    Serializer class for ServiceInstance collection
    """
    id = ObjectIdField(source='_id', read_only=True)  # ObjectIdField is read_only by default
    attributes = AttributesSerializer(required=False)

    def validate_attributes(self, attrs, source):
        if source in attrs:
            value = attrs[source]
            if value is None:
                bad_param = BadParameterValueException('null')
                raise ValidationError(bad_param.details)
        return attrs

    class Meta:
        schema = 'InstanceModel'
        view_item_name = 'instance_detail'
        url_fields = ('class_name', '_id')
        request_filter = settings.REQUEST_FILTER_PARAM
        mandatory_fields = ('uri', )
        # _id field of schema will be mapped in id
        exclude = ('_id',)


class ServiceInstanceItemSerializer(ServiceInstanceSerializer):
    id = ObjectIdField(source='_id', read_only=False)

    def restore_object(self, attrs, instance=None):
        try:
            instance = ServiceInstanceService().get_service_instance(self.context['class_name'],
                                                      self.context['id'])
            # Convert _id to string representation
            instance['_id'] = str(instance['_id'])
            # remove keys not present in attrs
            for key in instance.keys():
                if key not in attrs:
                    instance.pop(key)
        except NotFoundException as e:
            raise e
        return super(ServiceInstanceItemSerializer, self).restore_object(attrs, instance=instance)
