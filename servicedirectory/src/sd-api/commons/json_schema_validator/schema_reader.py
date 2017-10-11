'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''

from os.path import join, normpath
import json
from jsonschema import Draft4Validator, SchemaError, validate
from commons.exceptions import GenericServiceError
from commons.singleton import Singleton
import logging
import glob
from django.conf import settings
import sys

logger = logging.getLogger(__name__)


class SchemaField(object):

    def __init__(self, name=None, field_type=None, default=None, required=True, min_length=None, max_length=None,
                 min_value=None, max_value=None):
        self.name = name
        self.field_type = field_type
        self.default = default
        self.required = required
        self.min_length = min_length
        self.max_length = max_length
        self.min_value = min_value
        self.max_value = max_value


class SchemaReader(object):

    __metaclass__ = Singleton

    def __init__(self):
        self._schemas = {}
        self._get_all_schemas()

    def _get_all_schemas(self):
        """
        Reads json schemas folder, validate json schemas and sets
        internal _schemas variable for further use.
        """
        try:
            filePattern = normpath(join(settings.JSON_SCHEMAS_FOLDER, '*.json'))
        except AttributeError:
            logger.critical("Schemas path not found")
            raise GenericServiceError("Internal error. Try again later")
        files = glob.glob(filePattern)

        for filename in files:
            result = ''.join(open(filename).readlines())
            schema = json.loads(result)
            try:
                Draft4Validator.check_schema(schema)
                self._schemas[schema['title']] = schema
                logger.info("%s loaded.", filename)
            except SchemaError as e:
                logger.info(''.join([filename, " not loaded."]))
                logger.debug(str(e))
        logger.info("All schemas files loaded")

    def validate_object(self, obj, schema_name):
        # Validate with draf 3 in this way:
        # Draft3Validator(self.schemas[schema]).validate(obj )
        validate(obj, self.get_schema(schema_name))

    def validate_json_document(self, json_doc, schema_name):
        self.validate_object(json.loads(json_doc), schema_name)

    def get_schema(self, schema_name):
        try:
            return self._schemas[schema_name]
        except KeyError:
            msg = 'The json schema {0} is not found.'.format(schema_name)
            logger.critical(msg)
            raise GenericServiceError(msg)

    def get_schema_fields(self, schema_name):
        schema = self.get_schema(schema_name)
        fields = []
        if 'properties' in schema:
            for item_key, item_val in schema['properties'].items():
                required = item_key in schema.get('required', ())
                fields.append(SchemaField(item_key, item_val.get('type', None),
                                          item_val.get('default', None), required,
                                          item_val.get('minLength', None), item_val.get('maxLength', None),
                                          item_val.get('minimum', None), item_val.get('maximun', None)))
        return fields
