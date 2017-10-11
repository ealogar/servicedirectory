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
from re import match, compile
from sre_constants import error as CompileError
from django.conf import settings
from rest_framework.serializers import Serializer
from bson.objectid import ObjectId
from bson.errors import InvalidId
from django.core.exceptions import ValidationError
from bindings.services import BindingService

from commons.serializers import SchemaSerializer
from commons.exceptions import NotAllowedParameterValueException, BadParameterValueException, NotFoundException
from commons.fields import CharRestrictField, MultipleSerializerField,\
    RegexRestricField, ObjectIdField


logger = logging.getLogger(__name__)


class RuleSerializer(Serializer):
    operation = CharRestrictField(required=True)
    input_context_param = CharRestrictField(required=True, max_length=512, min_length=1)
    value = MultipleSerializerField(required=True, max_str_length=512, max_items=128, min_items=1)

    def validate_input_context_param(self, attrs, source):
        value = attrs[source]
        if not match(settings.INPUT_CONTEXT_KEYS_CREATE_REGEX, value):
            bad_param = BadParameterValueException(value)
            raise ValidationError(bad_param.details)
        return attrs

    def validate_operation(self, attrs, source):
        value = attrs[source]
        allowed = ('range', 'eq', 'in', 'regex')
        if value not in allowed:
            not_allowed = NotAllowedParameterValueException(value, str(allowed))
            raise ValidationError(not_allowed.details)
        return attrs

    def validate_value(self, attrs, source):
        # Validation of values depending on rules
        value = attrs[source]
        operation = attrs.get('operation', None)
        if operation == 'range':
            if len(value) != 2 or type(value[0]) != type(value[1]) or value[0] == value[1] or value[0] > value[1]:
                bad_param = BadParameterValueException(value)
                raise ValidationError(bad_param.details)
        elif operation == 'in':
            first_type_in = type(value[0])
            for elem in value[1:]:
                if type(elem) != first_type_in:
                    bad_param = BadParameterValueException(elem)
                    raise ValidationError(bad_param.details)
            try:
                unrepeated_set = set(value)
                if len(unrepeated_set) < len(value):
                    bad_param = BadParameterValueException(value)
                    raise ValidationError(bad_param.details)
            except TypeError:
                bad_param = BadParameterValueException(value)
                raise ValidationError(bad_param.details)
        elif operation == 'regex':
            bad_param = BadParameterValueException(value)
            if len(value) > 1:
                raise ValidationError(bad_param.details)
            try:
                compile(value[0])
            except CompileError:
                raise ValidationError(bad_param.details)
        elif operation == 'eq':
            if len(value) > 1:
                bad_param = BadParameterValueException(value)
                raise ValidationError(bad_param.details)

        return attrs


class BindingRulesSerializer(Serializer):
    group_rules = RuleSerializer(many=True, required=False)
    bindings = MultipleSerializerField(max_str_length=56, min_items=1, max_items=1, required=True)

    def validate_bindings(self, attrs, source):
        # To simplify, only size of one is allowed in bindings
        value = attrs.get(source, ())
        try:
            [ObjectId(instance) for instance in value]
        except (InvalidId, TypeError):
            bad_param = BadParameterValueException(instance)
            raise ValidationError(bad_param.details)
        return attrs


class BindingsSerializer(SchemaSerializer):

    id = ObjectIdField(source='_id', read_only=True)

    # class_name_regex is also used in url mapping, we need to slightly modify...
    class_name = RegexRestricField('^{0}$'.format(settings.CLASS_NAME_REGEX), min_length=1, max_length=512,
                                   required=True)
    origin = RegexRestricField(settings.ORIGIN_REGEX, min_length=1, max_length=512, required=True)
    binding_rules = BindingRulesSerializer(many=True)

    def validate_origin(self, attrs, source):
        """
        Check that origin:default in lowercase only
        """
        origin = attrs[source]
        if origin.lower() == 'default' and origin != 'default':
            bad_param = BadParameterValueException(origin)
            raise ValidationError(bad_param.details)
        return attrs

    class Meta:
        schema = 'Bindings'
        view_item_name = 'bindings_detail'
        url_fields = ('_id',)
        # _id field of schema will be mapped in id
        exclude = ('_id',)


class BindingInstanceSerializer(BindingsSerializer):
    id = ObjectIdField(source='_id', read_only=False)  # this parameter is taken from url id param...

    def restore_object(self, attrs, instance=None):
        try:
            instance = BindingService().get_binding_by_id(self.context['id'])
            # Convert _id to string representation
            instance['_id'] = str(instance['_id'])
            # remove keys not present in attrs
            for key in instance.keys():
                if key not in attrs:
                    instance.pop(key)
        except NotFoundException as e:
            raise e
        return super(BindingInstanceSerializer, self).restore_object(attrs, instance=instance)
