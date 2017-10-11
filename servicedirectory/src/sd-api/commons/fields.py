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
from rest_framework.fields import WritableField, IntegerField, BooleanField, CharField,\
    FloatField, RegexField
from django.core.exceptions import ValidationError
from commons.utils import convert_string_to_bool
from rest_framework.compat import six


EMPTY_VALUES = (None, [], (), {})

error_messages = {
    'required': 'required',
    'invalid': 'invalid'
}


# The following classed try to overcome some problems in django rest_framework
# They must be proposed to rest_framework as patches
class WritableRestrictField(WritableField):
    """
    Overrides Writable Field to avoid consider empty string as empty value.
    Note that this implementation is completely dependant on django rest-framework.
    """
    default_error_messages = error_messages

    def validate(self, value):
        if value in EMPTY_VALUES and self.required:
            raise ValidationError(self.error_messages['required'])

    def run_validators(self, value):
        if value in EMPTY_VALUES:
            return
        errors = []
        for v in self.validators:
            try:
                v(value)
            except ValidationError:
                errors.append(self.error_messages['invalid'])
        if errors:
            raise ValidationError(errors)


class BooleanRestrictField(WritableRestrictField, BooleanField):
    """
    Overrides BooleanField of rest framework to be restrict in accepted
    input values, only boolean valid strings will be acceptable
    """

    def from_native(self, value):
        if value is not None:
            if isinstance(value, bool):
                return value
            if isinstance(value, basestring):
                value = convert_string_to_bool(value, allow_flex_bolean=True)
                if value:
                    return value
        msg = self.error_messages['invalid']
        raise ValidationError(msg)


class CharRestrictField(WritableRestrictField, CharField):
    """
    SD version of CharField whic inherits from WritableRestricField
    to avoid consider empty string as empty_values.
    We take advantadge of multi inheritance where the override method
    in our WritableRestrictField will be called first.
    We also override from_native for not convert invalid strings to string
    using smart_text
    """

    def from_native(self, value):
        if isinstance(value, six.string_types) or value is None:
            return value
        raise ValidationError(self.error_messages['invalid'])


class IntegerRestrictField(WritableRestrictField, IntegerField):
    """
    Overrides IntegerField of rest_framework
    to avoid consider empty string as empty_values.
    We take advantadge of multi inheritance where the override method
    in our WritableRestrictField will be called first.
    """


class FloatRestrictField(WritableRestrictField, FloatField):
    """
    Overrides FloatField of rest_framework
    to avoid consider empty string as empty_values.
    We take advantadge of multi inheritance where the override method
    in our WritableRestrictField will be called first.
    """


class MultipleSerializerField(WritableRestrictField):
    """
    Just a serializer for arrays of basic types without validation or conversion of types.
    max_str_lenght can be used as kw args to specify the maximun lenght of the
    string representation of the object aka obj.__len__()
    """
    def __init__(self, max_str_length=56, max_items=256, min_items=0, **kw):
        self.max_str_length = max_str_length
        self.min_items = min_items
        self.max_items = max_items
        super(MultipleSerializerField, self).__init__(**kw)

    def to_native(self, obj):
        """
        We must return a list of objects
        """
        if isinstance(obj, list):
            return obj
        return super(MultipleSerializerField, self).to_native(obj)

    def validate(self, value):
        """
        Provide a extra validation here to check the value is a list of objects.
        from_native doesn't need to be provided here
        """
        if value and not isinstance(value, list):
            raise ValidationError(self.error_messages['invalid'])
        if len(value) < self.min_items or len(value) > self.max_items:
            raise ValidationError(self.error_messages['invalid'])
        # does not allow empty value and more thant max_str_length
        for elem in value:
            if elem in EMPTY_VALUES or elem == '':
                raise ValidationError(self.error_messages['invalid'])

            # for non unicode elemns, use str
            elem_len = len(elem) if hasattr(elem, '__len__') else len(str(elem))
            if  elem_len > self.max_str_length:
                raise ValidationError(self.error_messages['invalid'])
        super(MultipleSerializerField, self).validate(value)


class PasswordField(CharRestrictField):
    """
    Overrides from native to return *** in password protected
    """
    def to_native(self, obj):
        return "****"


class ObjectIdField(WritableRestrictField):

    """
    Field serializer for ObjectId of mongo DB.
    We dont override from_native to validate input string
    ast this will be done mainly by service logic.
    """
    def to_native(self, obj):
        return str(obj)


class RegexRestricField(WritableRestrictField, RegexField):
    """
    Overrides to run validators when empty values and
    define custome messages for validations
    """
    pass
