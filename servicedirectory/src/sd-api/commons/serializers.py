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
import functools
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import Serializer, SerializerOptions
from commons.exceptions import BadRequestException, \
    MissingMandatoryParameterException, BadParameterValueException, \
    NotAllowedParameterValueException
from commons.json_schema_validator.schema_reader import SchemaReader
from jsonschema import ValidationError as ValidationErrorSchema
import logging
from rest_framework.reverse import reverse
from django.utils.datastructures import SortedDict
from commons.fields import CharRestrictField, BooleanRestrictField, IntegerRestrictField, \
    FloatRestrictField, error_messages
from django.utils import six
from re import match

logger = logging.getLogger(__name__)


def deserialize_input(partial=False, validate=True):
    """
    Validate request.DATA and extra values provided in view using serializer class
    defined in view.
    deserialized_object keyword param will be added if succeded validation.

    If validation is not correct a Response error is thrown.
    If validation succeded, view method will be called.

    By default all serializer fields are required for validation; this can be changed
    using partial = True (for put methods when we don't want all validations).

    :param partial: Validate only informed fields in serializer
    :param validate: Don't run serializer validations

    """
    # Decorator defined inside to receive input params
    def applyDecorator(f):

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            called_view = args[0]
            request = args[1]
            # include fields not coming in request for validation
            # request.DATA: contains the query parameters + the body
            compose_data = request.DATA.copy()
            # kwargs. contains the url parameters
            compose_data.update(kwargs)
            # Get serializer and check data is valid
            serializer = called_view.get_serializer(data=compose_data, partial=partial)
            if validate and not serializer.is_valid():
                if '_schema_' in serializer.errors:
                    # Schema Validation error
                    raise BadParameterValueException(serializer.errors['_schema_'][0])

                # check for nested serializer errors and look inside errors array
                (key, value, text) = get_first_error(serializer.errors, compose_data)
                if error_messages['required'] in text:
                    raise MissingMandatoryParameterException(key)
                elif error_messages['invalid'] in text:
                    raise BadParameterValueException(value)
                elif match(NotAllowedParameterValueException.get_regex_unica_code(), text):
                    raise NotAllowedParameterValueException(None, None, details=text)
                elif match(BadParameterValueException.get_regex_unica_code(), text):
                    raise BadParameterValueException(None, details=text)
                else:
                    raise BadRequestException(text)
            # update request.DATA, request. and call the view
            kwargs['deserialized_object'] = serializer.object
            return f(called_view, request, **kwargs)
        return wrapper
    return applyDecorator


def get_first_error(errors, input_data):
    first_error = ('', '', unicode(errors))
    try:
        first_error = look_inside(errors, input_data)
    except Exception as e:
        logger.error("Error when generating formatted error message %s", str(e))
    return first_error


def look_inside(errors, input_data, parent_key=''):
    # Check this level of errors and get the first key
    for (key, values) in errors.items():
        if isinstance(values[0], six.string_types):
            if key == u'non_field_errors':
                return (parent_key, input_data, error_messages['invalid'])
            else:
                return (key, input_data.get(key, 'no_key'), values[0])
        else:
            # nested serializer error
            for i in range(0, len(values)):
                if isinstance(input_data[key], list):
                    res = look_inside(values[i], input_data[key][i], key)
                else:
                    res = look_inside(values[i], input_data[key], key)
                if res != None:
                    return res
            # Not found any error in nested error serializer-> unexpected
            return None
    # Not found any error in error
    return None


def generate_location_header(serializer, request):
    try:
        return {'Location': reverse(serializer.get_view_item_name(), request=request,
                  args=serializer.get_url_fields())}
    except Exception as e:
        logger.error('Error generating location Header %s', e)
        return {}


def serialize_to_response(many=False, status_code=status.HTTP_200_OK):
    """
    Serialize and object or a queryset (many=True) using serializer class and returns a valid
    representation of the object/queryset.
    If the view already returns a response, anything is done.
    """
    def applyDecorator(f):

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            called_object = args[0]

            # Get object or object list calling the function
            obj = f(*args, **kwargs)
            if not isinstance(obj, Response):
                # Serialize data and return Response
                serializer = called_object.get_serializer(obj, many=many)

                # Include location header when status is http_201_created
                headers = {}
                if status_code == status.HTTP_201_CREATED:
                    headers = generate_location_header(serializer, called_object.request)
                # When obj is None serializer.data fails
                resp_data = {}
                if obj is not None:
                    resp_data = serializer.data

                return Response(resp_data, status=status_code, headers=headers)
            else:
                # We have a rest_framework Response already, check if we must include location header
                if obj.status_code == status.HTTP_201_CREATED:
                    loc_header = generate_location_header(called_object.get_serializer(obj.data),
                                                          called_object.request)
                    obj['Location'] = loc_header['Location']

                return obj
        return wrapper
    return applyDecorator


class ExcludeFieldMixing(object):
    """
    Mixer utility for excluding fields in serialization based on request parameter for GET Method.
    It will take a comma separated values of fields given in a request parameter and
    would exclude then from serialization output.

    Request parameter is 'filter' by default, but can be overriden in meta serializer options.
    Mandatory fields can be defined too. It should be mixed with a Serializer.

    For example, when defining Meta Serializer options:
        class SerializerExcluded(ExcludeFieldMixing, ModelSerializer)
            class Meta:
                model = MyModel
                request_filter = 'filter'
                mandatory_fields = ['mandatory_field']

    """

    def __init__(self, *args, **kwargs):
        self.request_filter = getattr(self.Meta, 'request_filter', 'filter')
        self.mandatory_fields = getattr(self.Meta, 'mandatory_fields', ())
        super(ExcludeFieldMixing, self).__init__(*args, **kwargs)

    def get_fields(self, *args, **kwargs):
        """
        Override default for excluding fields based on filter parameter (if given)
        """
        # Check meta for override defaults
        if 'request' in getattr(self, 'context', None):
            request = self.context['request']
            if self.request_filter in getattr(request, 'QUERY_PARAMS', None)\
                and getattr(request, 'method', None) == 'GET':
                # Add mandatory fields
                read = super(ExcludeFieldMixing, self).get_fields(*args, **kwargs)
                _included = list(self.mandatory_fields)
                for including_fields in request.QUERY_PARAMS[self.request_filter].split(','):
                    if including_fields in read:
                        _included.append(including_fields)
                # Update required fields of serializer
                self.opts.fields = tuple(_included)
        return super(ExcludeFieldMixing, self).get_fields(*args, **kwargs)


class SchemaSerializerOptions(SerializerOptions):
    """
    Meta class options for SchemaSerializer
    """
    def __init__(self, meta):
        super(SchemaSerializerOptions, self).__init__(meta)
        self.schema = getattr(meta, 'schema', None)
        self.url_fields = getattr(meta, 'url_fields', ('_id',))
        self.view_item_name = getattr(meta, 'view_item_name', '')
        if self.schema is None:
            raise AttributeError('SchemaSerializer class must define a schema')


class SchemaSerializer(Serializer):
    """
    Overrides Serializer to include json schema validation before deserializing object.
    It also provides method for defining a url identified a given object (reverse).
    """
    default_error_messages = error_messages
    _options_class = SchemaSerializerOptions

    def json_schema_validation(self, instance):
        """
        Performs json schema validation for the given object
        according to schema defined in serializer.
        :param instance the object to run schema validation
        :return instance validated or None if Schema validation fails
        """
        try:
            SchemaReader().validate_object(instance, self.opts.schema)
        except ValidationErrorSchema as e:
            logger.info('Object not compliant with schema validation for Model %s', e.message)
            self._errors = self.fulfill_error_validation(e)
            return None
        return instance

    def fulfill_error_validation(self, error):
        """
        Helper function to parse a ValidationError from SchemaReader
        and convert to a readable message.
        When error is not a ValidationError the string representation
        will be returned.
        :param error the Exception to be read
        :return dictionary of key value for the Exception
        """
        # get key and message for output
        # TODO : iterate and return a full error schema to mix with input
        key = ''  # error.path may be empty if error happend at root of schema
        for key in reversed(error.path):
            if isinstance(key, basestring):
                break
        return {'_schema_': [error.instance]}

    def restore_object(self, attrs, instance=None):
        """
        Restore the dict object and validates json schema.
        :param attrs a dict with key,value to construct object
        :param instance a previous existing object (update operations)
        """

        if instance is not None:
            for key, val in attrs.items():
                instance[key] = val
        else:
            instance = dict(attrs)

        return self.json_schema_validation(instance)

    def get_url_fields(self):
        """
        """
        # Maybe put this in Meta

        url_fields_keys = self.opts.url_fields
        url_fields_values = []
        if self.object:
            for field_key in url_fields_keys:
                # get value from object or serializer context
                value = None
                if field_key in self.object:
                    value = self.object[field_key]
                elif field_key in self.context:
                    value = self.context[field_key]

                url_fields_values.append(value)
                if not value:
                    logger.error('The field %s is not available in object %s or view context',
                                   field_key, self.object)

        return url_fields_values

    def get_view_item_name(self):

        return self.opts.view_item_name

    def get_default_fields(self):
        """
        Return all the fields that should be serialized for the model.
        """

        schema = self.opts.schema
        schema_fields = SchemaReader().get_schema_fields(schema)

        ret = SortedDict()

        for schema_field in schema_fields:
            if schema_field.field_type == 'array':
                # TODO : Add support for arrays in schemas, nested serializers
                pass
            elif isinstance(schema_field.field_type, list):
                pass
            else:
                ret[schema_field.name] = self.get_field(schema_field)

        return ret

    def get_field(self, schema_field):
        """
        Creates a default instance of a basic schema field.
        """
        kwargs = {}

        kwargs['required'] = schema_field.required

        # TODO include read_only if possible
        # kwargs['read_only'] = True

        if schema_field.default is not None:
            kwargs['default'] = schema_field.default

        if schema_field.min_length is not None:
            kwargs['min_length'] = schema_field.min_length
        if schema_field.max_length is not None:
            kwargs['max_length'] = schema_field.max_length

        if schema_field.min_value is not None:
            kwargs['min_value'] = schema_field.min_value
        if schema_field.max_value is not None:
            kwargs['max_value'] = schema_field.max_value

        field_mapping = {
            'string': CharRestrictField,
            'boolean': BooleanRestrictField,
            'integer': IntegerRestrictField,
            'number': FloatRestrictField
            # TODO: Add support for nested schema
        }
        try:
            return field_mapping[schema_field.field_type](**kwargs)
        except KeyError:
            return CharRestrictField(**kwargs)

    def to_native(self, obj):
        """
        Override default to support serialization when not all elements are provided
        Serialize objects -> primitives.
        """
        # TODO in last version of rest_framework null is returned and not KeyError
        # TODO make this configurable depending on a serializer value
        ret = self._dict_class()
        ret.fields = {}

        for field_name, field in self.fields.items():
            field.initialize(parent=self, field_name=field_name)
            key = self.get_field_key(field_name)
            req_key = field.source or key
            if req_key not in obj:
                continue
            value = field.field_to_native(obj, field_name)
            ret[key] = value
            ret.fields[key] = field
        return ret
